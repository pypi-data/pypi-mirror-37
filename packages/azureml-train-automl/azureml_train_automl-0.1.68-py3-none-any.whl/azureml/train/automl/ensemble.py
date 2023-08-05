# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for ensembling previous AutoML iterations."""

import datetime
import numpy as np
import pickle
from sklearn.base import BaseEstimator
from sklearn.pipeline import make_pipeline

from automl.client.core.common import datasets
from automl.client.core.common import utilities
from automl.client.core.common import model_wrappers
from azureml.core import Experiment, Workspace, Run

from . import _automl_settings
from . import constants
from . import _ensemble_selector
from . import _logging


class Ensemble(BaseEstimator):
    """
    Class for ensembling previous AutoML iterations.
    The ensemble pipeline is initialized from a collection of already fitted pipelines.

    """

    def __init__(self,
                 automl_settings,
                 ensemble_run_id: str,
                 experiment_name: str,
                 workspace_name: str,
                 subscription_id: str,
                 resource_group_name: str):
        """Creates an Ensemble pipeline out of a collection of already fitted pipelines.

        Arguments:
            automl_settings -- The settings for this current experiment
            ensemble_run_id -- The id of the current ensembling run
            experiment_name -- The name of the current Azure ML experiment
            workspace_name --  The name of the current Azure ML workspace where the experiment is run
            subscription_id --  The id of the current Azure ML subscription where the experiment is run
            resource_group_name --  The name of the current Azure resource group
        """

        # input validation
        if automl_settings is None:
            raise ValueError("automl_settings parameter should not be None")

        if ensemble_run_id is None:
            raise ValueError("ensemble_run_id parameter should not be None")

        if experiment_name is None:
            raise ValueError("experiment_name parameter should not be None")

        if subscription_id is None:
            raise ValueError("subscription_id parameter should not be None")

        if resource_group_name is None:
            raise ValueError(
                "resource_group_name parameter should not be None")

        if workspace_name is None:
            raise ValueError("workspace_name parameter should not be None")

        self._ensemble_run_id = ensemble_run_id
        self._experiment_name = experiment_name
        self._subscription_id = subscription_id
        self._resource_group_name = resource_group_name
        self._workspace_name = workspace_name

        self._automl_settings = _automl_settings._AutoMLSettings.from_string_or_dict(automl_settings)

        if not hasattr(self._automl_settings, 'ensemble_iterations'):
            raise ValueError(
                "Need a configuration value for ensemble_iterations")

    def fit(self, X, y):
        """Fit method not implemented. Use the `fit_ensemble` method instead

        Raises:
            NotImplementedError -- Not using this API for ensemble training
        """
        raise NotImplementedError("call fit_ensemble instead")

    def fit_ensemble(self, training_type: constants.TrainingType, dataset: datasets.ClientDatasets, **kwargs):
        """
        Fits the ensemble based on the existing fitted pipelines.

        :param training_type: Type of training (eg: TrainAndValidate split, CrossValidation split, MonteCarlo, etc.)
        :type training_type: constants.TrainingType enumeration
        :param dataset: The training dataset.
        :type dataset: datasets.ClientDatasets
        :return: Returns a fitted ensemble including all the selected models.
        """

        logger = self._get_logger()

        # for the Ensemble selection we'll use the validation dataset (data the models haven't seen yet)
        X, y, sample_weight_valid = dataset.get_valid_set()
        ensemble_iterations = self._automl_settings.ensemble_iterations
        primary_metric = self._automl_settings.primary_metric

        parent_run = self._get_parent_run()
        child_runs = parent_run.get_children()

        task_type = self._automl_settings.task_type

        start = datetime.datetime.utcnow()
        algo_names, fitted_models = self._fetch_fitted_pipelines(
            logger, child_runs)
        elapsed = datetime.datetime.utcnow() - start
        logger.info("Fetched the fitted pipelines in {0} seconds".format(elapsed.seconds))

        start = datetime.datetime.utcnow()
        selector = _ensemble_selector.EnsembleSelector(logger=logger,
                                                       fitted_models=fitted_models,
                                                       metric=primary_metric,
                                                       iterations=ensemble_iterations,
                                                       task_type=task_type)

        unique_ensemble, unique_weights = selector.select(X, y, sample_weight_valid)
        elapsed = datetime.datetime.utcnow() - start
        logger.info("Selected the pipelines for the ensemble in {0} seconds".format(
            elapsed.seconds))

        # TODO: when creating the ensemble_estimator_tuples we'll need to
        # get the fully trained models (not the partially trained ones)
        ensemble_estimator_tuples = [(algo_names[i], fitted_models[i])
                                     for i in unique_ensemble]

        if task_type == constants.Tasks.CLASSIFICATION:
            # for the possible classes, we use the training dataset as the validation one might not contain all of them
            _, y_train, __ = dataset.get_train_set()
            unique_labels = np.unique(y_train).tolist()
            self.estimator = model_wrappers.PreFittedSoftVotingClassifier(estimators=ensemble_estimator_tuples,
                                                                          weights=unique_weights,
                                                                          classification_labels=unique_labels)
        elif task_type == constants.Tasks.REGRESSION:
            self.estimator = model_wrappers.PreFittedSoftVotingRegressor(estimators=ensemble_estimator_tuples,
                                                                         weights=unique_weights)
        return self.estimator

    def predict(self, X):
        """
        Predicts the target for the provided input.

        :param X: Input test samples.
        :type X: numpy.ndarray or scipy.spmatrix
        :return: Prediction values.
        """
        return self.estimator.predict(X)

    def predict_proba(self, X):
        """
        Returns the probability estimates for the input dataset.

        :param X: Input test samples.
        :type X: numpy.ndarray or scipy.spmatrix
        :return: Prediction probabilities values.
        """
        return self.estimator.predict_proba(X)

    def _get_parent_run(self):
        parent_run_id_length = self._ensemble_run_id.rindex("_")
        parent_run_id = self._ensemble_run_id[0:parent_run_id_length]

        if self._automl_settings.compute_target is not None and self._automl_settings.compute_target != 'local':
            # for remote runs we want to reuse the auth token from the environment variables
            current_run = Run.get_context()
            parent_run = Run(current_run.experiment, parent_run_id)
        else:
            workspace = Workspace(self._subscription_id, self._resource_group_name, self._workspace_name)
            experiment = Experiment(workspace, self._experiment_name)
            parent_run = Run(experiment, parent_run_id)

        return parent_run

    def _fetch_fitted_pipelines(self, logger, child_runs):
        local_model_file = "model.pkl"
        model_name = constants.MODEL_PATH
        fitted_pipelines = []
        algo_names = []

        logger.info("Fetching fitted models for all previous iterations")
        for child_run in child_runs:
            # we'll fetch all fitted models for all previously completed iterations
            # (except the Ensembling child iteration that was created earlier)
            if child_run.id == self._ensemble_run_id:
                continue
            try:
                properties = child_run.get_properties()
                algo_name = "Unknown"
                if 'run_algorithm' in properties:
                    algo_name = properties['run_algorithm']

                child_run.download_file(
                    name=model_name, output_file_path=local_model_file)
                with open(local_model_file, "rb") as model_file:
                    fitted_pipeline = pickle.load(model_file)

                fitted_pipelines.append(
                    self._transform_fitted_pipeline(fitted_pipeline))
                algo_names.append(algo_name)
            except Exception as e:
                logger.warning(
                    "Failed to read the fitted model for iteration {0}".format(child_run.id))
                utilities._log_traceback(e, logger)

        return algo_names, fitted_pipelines

    def _transform_fitted_pipeline(self, fitted_pipeline):

        # for performance reasons we'll transform the data only once inside the ensemble,
        # by adding the transformers to the ensemble pipeline (as preprocessor steps, inside automl.py).
        # Because of this, we need to remove any AutoML transformers from all the fitted pipelines here.
        modified_steps = [step[1] for step in fitted_pipeline.steps
                          if step[0] != "datatransformer" and step[0] != "laggingtransformer"]
        if len(modified_steps) != len(fitted_pipeline.steps):
            return make_pipeline(*[s for s in modified_steps])
        else:
            return fitted_pipeline

    def _get_logger(self):
        from . import _logging
        if self._automl_settings.compute_target is not None and self._automl_settings.compute_target != 'local':
            logger = _logging.get_logger(None, self._automl_settings.verbosity)
        else:
            logger = _logging.get_logger(
                self._automl_settings.debug_log, self._automl_settings.verbosity)

        return logger
