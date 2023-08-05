# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""AutoML object in charge of orchestrating various AutoML runs for predicting models."""
import json
import os
import os.path
import re
import sys
import warnings
from datetime import datetime
from importlib.util import module_from_spec, spec_from_file_location
from threading import Timer

import numpy as np
import pandas as pd
import pytz
import scipy
import sklearn
from automl.client.core.common import metrics, utilities, pipeline_spec
from automl.client.core.common.exceptions import (DataException,
                                                  ServiceException)
from automl.client.core.common.utilities import (_log_traceback,
                                                 _y_nan_check,
                                                 get_sdk_dependencies)
from msrest.exceptions import HttpOperationError

from azureml._restclient import JasmineClient, RunHistoryClient
from azureml._restclient.models.create_parent_run_dto import CreateParentRunDto
from azureml.core import Experiment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import RunConfiguration
from azureml.telemetry import get_diagnostics_collection_info

from . import _constants_azureml, _dataprep_utilities, automl, constants
from ._automl_settings import _AutoMLSettings
from ._console_interface import ConsoleInterface, RemoteConsoleInterface
from ._logging import cleanup_log_map, get_logger
from ._systemusage_telemetry import SystemResourceUsageTelemetryFactory
from .run import AutoMLRun
from .utilities import friendly_http_exception, _validate_training_data


class _AutoMLBase(object):
    """
    Client to run AutoML experiments on Azure Machine Learning platform
    """

    # Caches for querying and printing child runs
    run_map = {}
    metric_map = {}
    properties_map = {}

    def __init__(self,
                 experiment,
                 **kwargs):
        """
        Constructor for the _AutoMLBase class

        :param experiment: The azureml.core experiment
        :param kwargs: dictionary of keyword args
        :keyword something: something
        :keyword iterations: Number of different pipelines to test
        :keyword data_script: File path to the script containing get_data()
        :keyword primary_metric: The metric that you want to optimize.
        :keyword task_type: Field describing whether this will be a classification or regression experiment
        :keyword compute_target: The AzureML compute to run the AutoML experiment on
        :keyword validation_size: What percent of the data to hold out for validation
        :keyword n_cross_validations: How many cross validations to perform
        :keyword y_min: Minimum value of y for a regression experiment
        :keyword y_max: Maximum value of y for a regression experiment
        :keyword num_classes: Number of classes in the label data
        :keyword preprocess: Flag whether AutoML should preprocess your data for you
        :keyword lag_length: How many rows to lag data when preprocessing time series data
        :keyword max_cores_per_iteration: Maximum number of threads to use for a given iteration
        :keyword max_time_sec: Maximum time in seconds that each iteration before it terminates
        :keyword mem_in_mb: Maximum memory usage of each iteration before it terminates
        :keyword enforce_time_on_windows: flag to enforce time limit on model training at each iteration under windows.
        :keyword exit_time_sec: Maximum amount of time that all iterations combined can take
        :keyword exit_score: Target score for experiment. Experiment will terminate after this score is reached.
        :keyword blacklist_algos: List of algorithms to ignore for AutoML experiment
        :keyword exclude_nan_labels: Flag whether to exclude rows with NaN values in the label
        :keyword auto_blacklist: Flag whether AutoML should try to exclude algorithms
            that it thinks won't perform well.
        :keyword verbosity: Verbosity level for AutoML log file
        :keyword debug_log: File path to AutoML logs
        """

        if experiment is None:
            raise TypeError('AzureML experiment must be passed for AutoML.')

        self.automl_settings = _AutoMLSettings(experiment=experiment, **kwargs)

        self.experiment = experiment

        self._status = constants.Status.NotStarted
        self._loop = None
        self._score_max = None
        self._score_min = None
        self._score_best = None
        self._console_logger = open(os.devnull, "w")

        self.experiment_id = None
        self.parent_run_id = None
        self.current_iter = None
        self.pipelines = None
        self.input_data = None

        self._check_create_folders(self.automl_settings.path)
        self.logger = get_logger(
            self.automl_settings.debug_log, self.automl_settings.verbosity)

        send_telemetry, level = get_diagnostics_collection_info()
        self.automl_settings.telemetry_verbosity = level
        self.automl_settings.send_telemetry = send_telemetry
        self._usage_telemetry = SystemResourceUsageTelemetryFactory.get_system_usage_telemetry(
            self.logger)
        self._usage_telemetry.start()

        if not self.automl_settings.show_warnings:
            # sklearn forces warnings, so we disable them here
            warnings.simplefilter('ignore', DeprecationWarning)
            warnings.simplefilter('ignore', RuntimeWarning)
            warnings.simplefilter('ignore', UserWarning)
            warnings.simplefilter('ignore', FutureWarning)
            warnings.simplefilter(
                'ignore', sklearn.exceptions.UndefinedMetricWarning)

        data_script = self.automl_settings.data_script
        if data_script is not None:
            if os.path.exists(data_script):
                module_path = data_script
            else:
                if self.automl_settings.path is not None:
                    script_path = os.path.join(
                        self.automl_settings.path, data_script)
                    if os.path.exists(script_path):
                        module_path = script_path
                    else:
                        raise DataException("Could not find data script with name '{0}' or '{1}'"
                                            .format(data_script, script_path))
            try:
                #  Load user script to get access to GetData function
                spec = spec_from_file_location('get_data', module_path)
                self.user_script = module_from_spec(spec)
                spec.loader.exec_module(self.user_script)
                if not hasattr(self.user_script, 'get_data'):
                    raise DataException(
                        "User script does not contain get_data() function.")
                try:
                    self.input_data = utilities.extract_user_data(
                        self.user_script)
                    self._auto_blacklist(self.input_data)
                    if self.automl_settings.exclude_nan_labels:
                        self.input_data = _y_nan_check(self.input_data)
                except Exception:
                    pass
            except Exception as e:
                _log_traceback(e, self.logger)
                raise DataException(
                    "Could not import get_data() function from {0}".format(data_script)) from None
        else:
            self.user_script = None

        # Set up clients to communicate with AML services
        self._jasmine_client = JasmineClient(self.automl_settings.service_url,
                                             self.experiment.workspace._auth_object,
                                             self.experiment.workspace.subscription_id,
                                             self.experiment.workspace.resource_group,
                                             self.experiment.workspace.name,
                                             self.experiment.name)

        self._validation_scores = []

    def __del__(self):
        """
        Clean up AutoML loggers and close files.
        """
        cleanup_log_map(self.automl_settings.debug_log,
                        self.automl_settings.verbosity)

        if self._usage_telemetry is not None:
            self._usage_telemetry.stop()

    def start_experiment(self):
        """
        Start the AutoML experiment in AzureML run history.

        :return: None
        """
        try:

            # TODO: Review Service Call, the concepts here are very misused
            # PostProjectRun() (soon to be PostExperimentRun())
            experiment = self.experiment
            auth = experiment.workspace._auth_object
            subscription_id = experiment.workspace.subscription_id
            resource_group = experiment.workspace.resource_group
            workspace_name = experiment.workspace.name
            cloud_project_name = experiment.name

            run_history_client = RunHistoryClient(None,
                                                  auth,
                                                  subscription_id,
                                                  resource_group,
                                                  workspace_name,
                                                  cloud_project_name)
            run_history_client._prepare_experiment()

            self.experiment_id = self._jasmine_client.create_jasmine_experiment(
                self.automl_settings.name)
        except HttpOperationError as e:
            _log_traceback(e, self.logger)
            friendly_http_exception(e, constants.API.CreateExperiment)
        except Exception as e:
            _log_traceback(e, self.logger)
            raise ServiceException(
                "Error when trying to create experiment in AutoML service.") from None

        self.logger.info(
            'Jasmine created new experiment with id: \'{0}\''.format(self.experiment_id))
        self._status = constants.Status.Started

    def cancel(self):
        """
        Cancel the ongoing local run.

        :return: None
        """
        self._status = constants.Status.Terminated

    def fit(self,
            run_configuration=None,
            compute_target=None,
            X=None,
            y=None,
            sample_weight=None,
            X_valid=None,
            y_valid=None,
            sample_weight_valid=None,
            data=None,
            label=None,
            columns=None,
            cv_splits_indices=None,
            show_output=False,
            existing_run=False):
        """
        Start a new AutoML execution on the specified compute target

        :param run_configuration: The run confiuguration used by AutoML, should contain a compute target for remote
        :type run_configuration: Azureml.core RunConfiguration
        :param compute_target: The AzureML compute node to run this experiment on
        :type compute_target: azureml.core.compute.AbstractComputeTarget
        :param X: Training features
        :type X: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
        :param y: Training labels
        :type y: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
        :param sample_weight:
        :type sample_weight: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
        :param X_valid: validation features
        :type X_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
        :param y_valid: validation labels
        :type y_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
        :param sample_weight_valid: validation set sample weights
        :type sample_weight_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
        :param data: Training features and label
        :type data: pandas.DataFrame
        :param label: Label column in data
        :type label: str
        :param columns: whitelist of columns in data to use as features
        :type columns: list(str)
        :param cv_splits_indices: Indices where to split training data for cross validation
        :type cv_splits_indices: list(int), or list(Dataflow) in which each Dataflow represent a train-valid set
                                 where 1 indicates record for training and 0 indicates record for validation
        :param show_output: Flag whether to print output to console
        :type show_output: bool
        :return: AutoML parent run
        :rtype: azureml.train.automl.AutoMLRun
        """
        if show_output:
            self._console_logger = sys.stdout

        if run_configuration is None:
            run_configuration = RunConfiguration()
            if compute_target is not None:
                run_configuration.name = compute_target.name
                self._console_logger.write('No run_configuration provided, running on {0} with default configuration\n'
                                           .format(compute_target.name))
            else:
                self._console_logger.write(
                    'No run_configuration provided, running locally with default configuration\n')

        self.automl_settings.compute_target = run_configuration.target

        if run_configuration.target == 'local':
            if self.automl_settings.path is None:
                self.automl_settings.path = '.'
            name = run_configuration._name if run_configuration._name else "local"
            run_configuration.save(self.automl_settings.path, name)

            return self._fit_local(X=X, y=y, sample_weight=sample_weight, X_valid=X_valid, y_valid=y_valid, data=data,
                                   label=label, columns=columns, cv_splits_indices=cv_splits_indices,
                                   existing_run=existing_run, sample_weight_valid=sample_weight_valid)
        self._console_logger.write(
            'Running on remote compute: ' + str(run_configuration.target) + '\n')

        return self._fit_remote(run_configuration, X=X, y=y, sample_weight=sample_weight, X_valid=X_valid,
                                y_valid=y_valid, sample_weight_valid=sample_weight_valid,
                                cv_splits_indices=cv_splits_indices, show_output=show_output)

    def _fit_local(self, X=None, y=None, sample_weight=None, X_valid=None, y_valid=None, sample_weight_valid=None,
                   data=None, label=None, columns=None, cv_splits_indices=None, existing_run=False):
        """
        Main logic for executing a local AutoML experiment
        :return: AutoML parent run
        :rtype: azureml.train.automl.AutoMLRun
        """
        #  Prepare data before entering for loop
        self.logger.info("Extracting user Data")
        if X is None and y is None and data is None:
            if self.input_data is None:
                self.input_data = utilities.extract_user_data(self.user_script)
            X = self.input_data['X']
            y = self.input_data['y']
            sample_weight = self.input_data['sample_weight']
            X_valid = self.input_data['X_valid']
            y_valid = self.input_data['y_valid']
            sample_weight_valid = self.input_data['sample_weight_valid']
            cv_splits_indices = self.input_data["cv_splits_indices"]
        elif data is not None and label is not None:
            # got pandas DF
            X = data[data.columns.difference([label])]
            if columns is not None:
                X = X[X.columns.intersection(columns)]
            y = data[label].values

            # Get the raw column names
            x_raw_column_names = None
            if isinstance(X, pd.DataFrame):
                # Cache the raw column names if available
                x_raw_column_names = X.columns.values

            self.input_data = {
                'X': X,
                'y': y,
                'X_valid': X_valid,
                'y_valid': y_valid,
                'cv_splits_indices': cv_splits_indices,
                'x_raw_column_names': x_raw_column_names,
                'sample_weight': sample_weight,
                'sample_weight_valid': sample_weight_valid}
        else:
            # Get the raw column names
            x_raw_column_names = None
            if isinstance(X, pd.DataFrame):
                # Cache the raw column names if available
                x_raw_column_names = X.columns.values
            else:
                X = _dataprep_utilities.try_retrieve_pandas_dataframe(X)
                y = _dataprep_utilities.try_retrieve_numpy_array(y)
                sample_weight = _dataprep_utilities.try_retrieve_numpy_array(
                    sample_weight)
                X_valid = _dataprep_utilities.try_retrieve_pandas_dataframe(
                    X_valid)
                y_valid = _dataprep_utilities.try_retrieve_numpy_array(y_valid)
                sample_weight_valid = _dataprep_utilities.try_retrieve_numpy_array(
                    sample_weight_valid)
                cv_splits_indices = _dataprep_utilities.try_resolve_cv_splits_indices(
                    cv_splits_indices)

            self.input_data = {
                'X': X,
                'y': y,
                'X_valid': X_valid,
                'y_valid': y_valid,
                'cv_splits_indices': cv_splits_indices,
                'x_raw_column_names': x_raw_column_names,
                'sample_weight': sample_weight,
                'sample_weight_valid': sample_weight_valid}

        # todo put in helper, same as above code
        if isinstance(X, pd.DataFrame):
            X = X.values
            self.input_data['X'] = X
        if isinstance(y, pd.DataFrame):
            y = y.values
            self.input_data['y'] = y
        if isinstance(X_valid, pd.DataFrame):
            X_valid = X_valid.values
            self.input_data['X_valid'] = X_valid
        if isinstance(y_valid, pd.DataFrame):
            y_valid = y_valid.values
            self.input_data['y_valid'] = y_valid
        if isinstance(sample_weight, pd.DataFrame):
            sample_weight = sample_weight.values
            self.input_data['sample_weight'] = sample_weight
        if isinstance(sample_weight_valid, pd.DataFrame):
            sample_weight_valid = sample_weight_valid.values
            self.input_data['sample_weight'] = sample_weight_valid

        # Validate X, y and sample_weight
        _validate_training_data(X, y, X_valid, y_valid, sample_weight, sample_weight_valid,
                                cv_splits_indices, self.automl_settings)

        self._auto_blacklist(self.input_data)
        if self.automl_settings.exclude_nan_labels:
            self.input_data = _y_nan_check(self.input_data)
            X = self.input_data['X']
            y = self.input_data['y']
            sample_weight = self.input_data['sample_weight']
            X_valid = self.input_data['X_valid']
            y_valid = self.input_data['y_valid']
            sample_weight_valid = self.input_data['sample_weight_valid']

        self._set_task_parameters(y=y)

        if not existing_run:
            # Call Jasmine to create experiment and parent run history entries
            parent_run_dto = CreateParentRunDto(target='local',
                                                num_iterations=self.automl_settings.iterations,
                                                training_type=None,  # use self.training_type when jasmine supports it
                                                acquisition_function=None,
                                                metrics=['accuracy'],
                                                primary_metric=self.automl_settings.primary_metric,
                                                train_split=self.automl_settings.validation_size,
                                                max_time_seconds=self.automl_settings.max_time_sec,
                                                acquisition_parameter=0.0,
                                                num_cross_validation=self.automl_settings.n_cross_validations,
                                                raw_aml_settings_string=str(
                                                    self.automl_settings.__dict__),
                                                aml_settings_json_string=json.dumps(self.automl_settings.__dict__))
            try:
                self.logger.info(
                    "Start creating parent run with DTO: {0}.".format(parent_run_dto))
                self.parent_run_id = self._jasmine_client.post_parent_run(
                    self.automl_settings.name, parent_run_dto)
            except HttpOperationError as e:
                _log_traceback(e, self.logger)
                friendly_http_exception(e, constants.API.CreateParentRun)
            except Exception as e:
                _log_traceback(e, self.logger)
                raise ServiceException(
                    "Error when trying to create parent run in automl service") from None
        self.current_run = AutoMLRun(self.experiment,
                                     self.parent_run_id,
                                     host=self.automl_settings.service_url)

        dependencies = {'dependencies_versions': None}
        dependencies['dependencies_versions'] = json.dumps(
            get_sdk_dependencies())
        self.current_run.add_properties(dependencies)

        self._console_logger.write("Parent Run ID: " + self.parent_run_id)
        self.logger.info("Parent Run ID: " + self.parent_run_id)

        self._status = constants.Status.InProgress

        if not existing_run:
            self._jasmine_client.set_parent_run_status(
                self.parent_run_id, constants.RunState.START_RUN)

            # set the problem info, so the JOS can use it to get pipelines.
            automl.set_problem_info(X, y, self.automl_settings.task_type,
                                    current_run=self.current_run,
                                    preprocess=self.automl_settings.preprocess,
                                    lag_length=self.automl_settings.lag_length)

        if self.automl_settings.exit_time_sec is not None:
            Timer(self.automl_settings.exit_time_sec, self.cancel).start()

        try:
            #  Set up interface to print execution progress
            ci = ConsoleInterface("score", self._console_logger)
            ci.print_descriptions()
            ci.print_columns()
        except Exception as e:
            _log_traceback(e, self.logger)
            raise
        if existing_run:
            self.current_iter = len(
                list(self.current_run.get_children(_rehydrate_runs=False)))
            self.pipelines = [(constants.Defaults.DEFAULT_PIPELINE_SCORE,
                               constants.Defaults.INVALID_PIPELINE_FITTED,
                               constants.Defaults.INVALID_PIPELINE_FITTED,
                               constants.Defaults.INVALID_PIPELINE_VALIDATION_SCORES,
                               None)] * self.current_iter
        else:
            self.current_iter = 0
            self.pipelines = []
        try:
            self.logger.info("Start local loop.")
            bad_scores = metrics.get_worst_values(
                self.automl_settings.task_type)
            bad_score = 0.0
            if self.automl_settings.primary_metric in bad_scores:
                bad_score = bad_scores[self.automl_settings.primary_metric]

            while self.current_iter < self.automl_settings.iterations:
                self.logger.info(
                    "Start iteration: {0}".format(self.current_iter))
                if (self._status == constants.Status.Terminated):
                    self._console_logger.write(
                        "Stopping criteria reached at iteration {0}. Ending experiment.".format(self.current_iter))
                    self.logger.info("Stopping criteria reached at iteration {0}. "
                                     "Ending experiment.".format(self.current_iter))
                    self._jasmine_client.set_parent_run_status(
                        self.parent_run_id, constants.RunState.CANCEL_RUN)
                    return AutoMLRun(self.experiment, self.parent_run_id, host=self.automl_settings.service_url)
                self._fit_iteration(ci, X, y, sample_weight, X_valid, y_valid,
                                    sample_weight_valid, cv_splits_indices,
                                    default_score=bad_score,
                                    remaining_parameters_dict=self.input_data)
            # create the AutoML Run object eagerly so that we can create a
            # child iteration for ensembling (if required)
            self.current_run = AutoMLRun(
                self.experiment, self.parent_run_id, host=self.automl_settings.service_url)

            # ensembling iteration
            if self.automl_settings.enable_ensembling:
                self._ensembling_iteration(ci, X, y, sample_weight, X_valid, y_valid,
                                           sample_weight_valid, cv_splits_indices)

            self._status = constants.Status.Completed
        except KeyboardInterrupt:
            self._status = constants.Status.Terminated
            self.logger.info("Received interrupt. Returning now.")
            self._console_logger.write("Received interrupt. Returning now.")
            self._jasmine_client.set_parent_run_status(
                self.parent_run_id, constants.RunState.CANCEL_RUN)
        finally:
            if not existing_run and self._status != constants.Status.Terminated:
                self._jasmine_client.set_parent_run_status(
                    self.parent_run_id, constants.RunState.COMPLETE_RUN)

        self.logger.info("Run Complete.")
        return self.current_run

    def _ensembling_iteration(self, ci, X, y, sample_weight, X_valid, y_valid, sample_weight_valid,
                              cv_splits_indices=None):
        ci.print_start(self.current_iter)
        start_iter_time = datetime.utcnow()
        validation_scores = {'metrics': None}

        pipeline_id = constants.ENSEMBLE_PIPELINE_ID
        ensemble_run_id = "{0}_{1}".format(
            self.parent_run_id, self.current_iter)
        spec_dict = {
            "pipeline_id": pipeline_id,
            "objects": [{
                "module": "azureml.train.automl.ensemble",
                "class_name": "Ensemble",
                "spec_class": pipeline_spec.SKLEARN_NAME,
                "param_args": (),
                "param_kwargs": {
                        "automl_settings": str(self.automl_settings.__dict__),
                        "ensemble_run_id": ensemble_run_id,
                        "experiment_name": self.experiment.name,
                        "workspace_name": self.experiment.workspace.name,
                        "subscription_id": self.experiment.workspace.subscription_id,
                        "resource_group_name": self.experiment.workspace.resource_group
                        }}]}

        pipeline_script = json.dumps(spec_dict)
        tags = self.current_run.get_tags()

        if 'iterations' in tags:
            iterations = int(tags['iterations'])
        else:
            iterations = int(self.automl_settings.iterations)

        self.automl_settings.iterations = iterations + 1
        self.current_run.tag('iterations', str(
            self.automl_settings.iterations))

        current_run = self.current_run.child_run(
            name="Ensembling run", run_id=ensemble_run_id)
        properties = {
            "iteration": str(self.current_iter),
            "runTemplate": "automl_child",
            "pipeline_id": pipeline_id,
            "pipeline_spec": pipeline_script
        }
        current_run.add_properties(properties)

        validation_scores = automl.fit_pipeline(pipeline_script,
                                                self.automl_settings,
                                                ensemble_run_id,
                                                X,
                                                y,
                                                sample_weight,
                                                X_valid=X_valid,
                                                y_valid=y_valid,
                                                sample_weight_valid=sample_weight_valid,
                                                cv_splits_indices=cv_splits_indices,
                                                fit_iteration_parameters_dict=None,
                                                experiment=self.experiment,
                                                iteration=self.current_iter,
                                                pipeline_id=pipeline_id,
                                                experiment_id=self.experiment_id,
                                                score_max=self._score_max,
                                                score_min=self._score_min,
                                                remote=False,
                                                logger=self.logger)
        # check the iteration for any errors
        if len(validation_scores['errors']) > 0:
            err_type = next(iter(validation_scores['errors']))
            inner_ex = validation_scores['errors'][err_type]['exception']
            raise RuntimeError(inner_ex) from inner_ex

        self._validation_scores.insert(self.current_iter, validation_scores)
        score = float(validation_scores[self.automl_settings.primary_metric])
        fitted_pipeline = validation_scores['fitted_pipeline']

        ci.print_pipeline("Ensemble")

        self._update_internal_scores_after_iteration(score)

        self.pipelines.append((score,
                               "Ensemble pipeline",
                               fitted_pipeline,
                               validation_scores,
                               AutoMLRun(self.experiment,
                                         self.parent_run_id,
                                         host=self.automl_settings.service_url)))
        end_iter_time = datetime.utcnow()
        start_iter_time = start_iter_time.replace(tzinfo=pytz.UTC)
        end_iter_time = end_iter_time.replace(tzinfo=pytz.UTC)
        iter_duration = str(end_iter_time - start_iter_time)
        ci.print_end(iter_duration, score, self._score_best)

        self.current_iter += 1

    def _fit_iteration(self, ci, X, y, sample_weight, X_valid, y_valid,
                       sample_weight_valid, cv_splits_indices=None,
                       default_score=float('nan'), remaining_parameters_dict=None):
        # TODO once JOS returns only valid pipelines for the problem space
        start_iter_time = datetime.utcnow()

        #  Query Jasmine for the next set of pipelines to run
        try:
            self.logger.info("Querying Jasmine for next pipeline.")
            pipeline_dto = self._get_pipeline()
        except HttpOperationError as e:
            _log_traceback(e, self.logger)
            friendly_http_exception(e, constants.API.GetNextPipeline)
        except Exception as e:
            _log_traceback(e, self.logger)
            raise ServiceException(
                "Error occurred when trying to fetch next iteration from AutoML service.") from None

        run_id = pipeline_dto.childrun_id
        pipeline_id = pipeline_dto.pipeline_id
        pipeline_script = pipeline_dto.pipeline_spec
        # print(pipeline_script)
        self.logger.info("Received pipeline: {0}".format(pipeline_script))

        ci.print_start(self.current_iter)
        validation_scores = {'metrics': None}
        error = None
        try:
            validation_scores = automl.fit_pipeline(pipeline_script,
                                                    self.automl_settings,
                                                    run_id,
                                                    X,
                                                    y,
                                                    sample_weight,
                                                    X_valid=X_valid,
                                                    y_valid=y_valid,
                                                    sample_weight_valid=sample_weight_valid,
                                                    cv_splits_indices=cv_splits_indices,
                                                    fit_iteration_parameters_dict=remaining_parameters_dict,
                                                    experiment=self.experiment,
                                                    iteration=self.current_iter,
                                                    pipeline_id=pipeline_id,
                                                    experiment_id=self.experiment_id,
                                                    score_max=self._score_max,
                                                    score_min=self._score_min,
                                                    remote=False,
                                                    logger=self.logger)

            if len(validation_scores['errors']) > 0:
                err_type = next(iter(validation_scores['errors']))
                inner_ex = validation_scores['errors'][err_type]['exception']
                raise RuntimeError("Parent run '{0}' failed. Check {1} for more details."
                                   .format(self.parent_run_id, self.automl_settings.debug_log)) from inner_ex

            self._validation_scores.insert(
                self.current_iter, validation_scores)
            if validation_scores is None or len(validation_scores) == 0:
                raise RuntimeError("Fit failed for this iteration for unknown reasons. Check {0} "
                                   "for more details.".format(self.automl_settings.debug_log))
            score = float(
                validation_scores[self.automl_settings.primary_metric])
            fitted_pipeline = validation_scores['fitted_pipeline']
            pipeline_script = validation_scores['pipeline_spec']
            pipeline_obj = validation_scores['pipeline_python_obj']
        except Exception as e:
            _log_traceback(e, self.logger)
            score = default_score
            self._validation_scores.insert(
                self.current_iter, constants.Defaults.INVALID_PIPELINE_VALIDATION_SCORES)
            fitted_pipeline = constants.Defaults.INVALID_PIPELINE_FITTED
            pipeline_obj = constants.Defaults.INVALID_PIPELINE_OBJECT
            error = e

        ci.print_pipeline(utilities._make_printable(pipeline_obj))
        self._update_internal_scores_after_iteration(score)

        self.pipelines.append((score,
                               pipeline_script,
                               fitted_pipeline,
                               validation_scores,
                               AutoMLRun(self.experiment,
                                         self.parent_run_id,
                                         host=self.automl_settings.service_url)))

        end_iter_time = datetime.utcnow()
        start_iter_time = start_iter_time.replace(tzinfo=pytz.UTC)
        end_iter_time = end_iter_time.replace(tzinfo=pytz.UTC)
        iter_duration = str(end_iter_time - start_iter_time)
        ci.print_end(iter_duration, score, self._score_best)
        self.current_iter = self.current_iter + 1

        if error is not None:
            ci.print_error(error)

        if self.automl_settings.exit_score is not None and isinstance(score, float):
            if self.automl_settings.metric_operation == constants.OptimizerObjectives.MINIMIZE:
                if score < self.automl_settings.exit_score:
                    self.cancel()
            elif self.automl_settings.metric_operation == constants.OptimizerObjectives.MAXIMIZE:
                if score > self.automl_settings.exit_score:
                    self.cancel()

    def _fit_remote(self, run_configuration, X=None, y=None, sample_weight=None, X_valid=None, y_valid=None,
                    sample_weight_valid=None, cv_splits_indices=None, show_output=False):
        if isinstance(run_configuration, str):
            run_config_object = RunConfiguration.load(
                self.automl_settings.path, run_configuration)
        else:
            # we alread have a run configuration object
            run_config_object = run_configuration
            run_configuration = run_config_object.target

        run_config_object = self._modify_run_configuration(run_config_object)

        dataprep_json = None
        df_value_list = [X, y, sample_weight, X_valid,
                         y_valid, sample_weight_valid, cv_splits_indices]
        if any(var is not None for var in df_value_list):
            def raise_type_error():
                raise ValueError("Passing X, y, sample_weight, X_valid, y_valid, sample_weight_valid or " +
                                 "cv_splits_indices as data to fit is only supported for local runs. For " +
                                 "remote runs, please provide X, y, sample_weight, X_valid, y_valid, " +
                                 "sample_weight_valid and cv_splits_indices as azureml.dataprep.Dataflow " +
                                 "objects, or provide a get_data() file instead.")
            dataflow_dict = {
                'X': X,
                'y': y,
                'sample_weight': sample_weight,
                'X_valid': X_valid,
                'y_valid': y_valid,
                'sample_weight_valid': sample_weight_valid
            }
            for i in range(len(cv_splits_indices or [])):
                split = cv_splits_indices[i]
                if not _dataprep_utilities.is_dataflow(split):
                    raise_type_error()
                else:
                    dataflow_dict['cv_splits_indices_{0}'.format(i)] = split
            dataprep_json = _dataprep_utilities.save_dataflows_to_json(
                dataflow_dict)
            if dataprep_json is None:
                raise_type_error()

        parent_run_dto = CreateParentRunDto(target=run_configuration,
                                            num_iterations=self.automl_settings.iterations,
                                            training_type=None,  # use self.training_type when jasmine supports it
                                            acquisition_function=None,
                                            metrics=['accuracy'],
                                            primary_metric=self.automl_settings.primary_metric,
                                            train_split=self.automl_settings.validation_size,
                                            max_time_seconds=self.automl_settings.max_time_sec,
                                            acquisition_parameter=0.0,
                                            num_cross_validation=self.automl_settings.n_cross_validations,
                                            raw_aml_settings_string=str(
                                                self.automl_settings.__dict__),
                                            aml_settings_json_string=json.dumps(
                                                self.automl_settings.__dict__),
                                            data_prep_json_string=dataprep_json)

        try:
            self.logger.info(
                "Start creating parent run with DTO: {0}.".format(parent_run_dto))
            self.parent_run_id = self._jasmine_client.post_parent_run(
                self.automl_settings.name, parent_run_dto)
        except HttpOperationError as e:
            _log_traceback(e, self.logger)
            friendly_http_exception(e, constants.API.CreateParentRun)
        except Exception as e:
            _log_traceback(e, self.logger)
            raise ServiceException(
                "Error occurred when tyring to create new parent run in AutoML service.") from None
        self.current_run = AutoMLRun(
            self.experiment, self.parent_run_id, host=self.automl_settings.service_url)
        self._console_logger.write("Parent Run ID: " + self.parent_run_id)
        self.logger.info("Parent Run ID: " + self.parent_run_id)

        snapshotId = self.current_run.take_snapshot(self.automl_settings.path)
        self.logger.info("Snapshotted folder: {0} with snapshot_id: {1}".format(
            self.automl_settings.path, snapshotId))

        self.pipelines = []

        definition = {
            "Configuration": RunConfiguration._serialize_to_dict(run_config_object)
        }

        # BUG: 287204
        del definition["Configuration"]["environment"]["python"]["condaDependenciesFile"]
        definition["Configuration"]["environment"]["python"]["condaDependencies"] = \
            run_config_object.environment.python.conda_dependencies._conda_dependencies

        self.logger.info("Starting a snapshot run (snapshotId : {0}) with following compute definition: {1}"
                         .format(snapshotId, definition))
        try:
            self._jasmine_client.post_remote_jasmine_snapshot_run(self.parent_run_id,
                                                                  json.dumps(
                                                                      definition),
                                                                  snapshotId)
        except HttpOperationError as e:
            _log_traceback(e, self.logger)
            friendly_http_exception(e, constants.API.StartRemoteSnapshotRun)
        except Exception as e:
            _log_traceback(e, self.logger)
            raise ServiceException("Error occured when tyring to submit a remote run to AutoML Service.") \
                from None

        self.current_run = AutoMLRun(
            self.experiment, self.parent_run_id, host=self.automl_settings.service_url)
        if show_output:
            try:
                if self.automl_settings.enable_ensembling:
                    # we would want the console printer to wait for the ensemble iteration as well.
                    total_iterations = self.automl_settings.iterations + 1
                else:
                    total_iterations = self.automl_settings.iterations

                remote_printer = RemoteConsoleInterface(
                    self._console_logger, self.logger)
                remote_printer.print(self.current_run,
                                     self.automl_settings.primary_metric,
                                     total_iterations)
            except KeyboardInterrupt:
                self._console_logger.write(
                    "Received interrupt. Returning now.")
        return self.current_run

    def _auto_blacklist(self, output):
        if self.automl_settings.auto_blacklist:
            X = output['X']
            if scipy.sparse.issparse(X) or len(X) > constants.MAX_SAMPLES_BLACKLIST:
                if self.automl_settings.blacklist_algos is None:
                    self.automl_settings.blacklist_algos = constants.MAX_SAMPLES_BLACKLIST_ALGOS
                else:
                    for blacklist_algo in constants.MAX_SAMPLES_BLACKLIST_ALGOS:
                        if blacklist_algo not in self.automl_settings.blacklist_algos:
                            self.automl_settings.blacklist_algos.append(
                                blacklist_algo)
                self.automl_settings.blacklist_samples_reached = True

    def _get_pipeline(self):
        """
        Query Jasmine for the next set of pipelines

        :param pipelines: Previously run pipelines and their scores
        :type pipelines: PipelineDto
        :return: List of pipeline specs to evaluate next
        """
        pipeline_out_dto = self._jasmine_client.get_pipeline(
            self.parent_run_id, self.current_iter)
        return pipeline_out_dto

    def _get_best_pipeline_score(self, validation_scores):
        """

        :return: the best score based on the metric objective
        """
        if self.automl_settings.metric_operation == constants.OptimizerObjectives.MINIMIZE:
            return np.nanmin(validation_scores)
        elif self.automl_settings.metric_operation == constants.OptimizerObjectives.MAXIMIZE:
            return np.nanmax(validation_scores)
        raise NotImplementedError()

    def _set_task_parameters(self, y):
        """

        :param y:
        :return:
        """
        if self.automl_settings.task_type == constants.Tasks.CLASSIFICATION:
            #  Guess number of classes if the user did not explicitly provide
            #  it
            if (not self.automl_settings.num_classes or not isinstance(self.automl_settings.num_classes, int)):
                self.automl_settings.num_classes = len(np.unique(y))
            return

        if self.automl_settings.task_type == constants.Tasks.REGRESSION:
            numpy_unserializable_ints = (np.int8, np.int16, np.int32, np.int64,
                                         np.uint8, np.uint16, np.uint32, np.uint64)

            #  Guess min and max of y if the user did not explicitly provide it
            if (not self.automl_settings.y_min or not isinstance(self.automl_settings.y_min, float)):
                self.automl_settings.y_min = np.min(y)
                if isinstance(self.automl_settings.y_min, numpy_unserializable_ints):
                    self.automl_settings.y_min = int(
                        self.automl_settings.y_min)
            if (not self.automl_settings.y_max or not isinstance(self.automl_settings.y_max, float)):
                self.automl_settings.y_max = np.max(y)
                if isinstance(self.automl_settings.y_max, numpy_unserializable_ints):
                    self.automl_settings.y_max = int(
                        self.automl_settings.y_max)
            assert self.automl_settings.y_max != self.automl_settings.y_min
            return
        raise NotImplementedError()

    def _check_create_folders(self, path):
        if path is not None and not os.path.exists(os.path.join(os.getcwd(), path)):
            os.makedirs(os.path.join(path, "aml_config"))
        elif not os.path.exists(os.path.join(os.getcwd(), "aml_config")):
            os.makedirs(os.path.join(os.getcwd(), "aml_config"))

    def _modify_run_configuration(self, run_config):
        """
        Takes a run_config object ensures our conda dependencies exist
        """
        run_config.auto_prepare_environment = True

        dependencies = run_config.environment.python.conda_dependencies
        if self.automl_settings.sdk_url is not None:
            dependencies.set_pip_option("--extra-index-url " + self.automl_settings.sdk_url)

        if self.automl_settings.sdk_packages is not None:
            for package in self.automl_settings.sdk_packages:
                dependencies.add_pip_package(package)

        automl_regex = r"azureml\S*automl\S*"
        numpy_regex = r"numpy([\=\<\>\~0-9\.\s]+|\Z)"

        if not re.findall(numpy_regex, " ".join(dependencies.conda_packages)):
            dependencies.add_conda_package("numpy")

        if not re.findall(automl_regex, " ".join(dependencies.pip_packages)):
            dependencies.add_pip_package("azureml-train-automl")

        run_config.environment.python.conda_dependencies = dependencies
        return run_config

    def _update_internal_scores_after_iteration(self, score):
        if self._score_max is None or np.isnan(self._score_max) or score > self._score_max:
            self._score_max = score
        if self._score_min is None or np.isnan(self._score_min) or score < self._score_min:
            self._score_min = score

        if self.automl_settings.metric_operation == constants.OptimizerObjectives.MINIMIZE:
            self._score_best = self._score_min
        elif self.automl_settings.metric_operation == constants.OptimizerObjectives.MAXIMIZE:
            self._score_best = self._score_max
