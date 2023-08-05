# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The AutoML Run object."""
import json
import logging
import os
import pickle
import sys
import time

import numpy as np
import pandas as pd
from automl.client.core.common.exceptions import ServiceException
from automl.client.core.common.metrics import minimize_or_maximize
from automl.client.core.common.utilities import (_all_dependencies,
                                                 _check_dependencies_versions,
                                                 _get_max_min_comparator,
                                                 get_sdk_dependencies)
from msrest.exceptions import HttpOperationError

from azureml._restclient import JasmineClient
from azureml._restclient.utils import camel_case_transformer
from azureml.core import Run, ScriptRun
from azureml.core.model import Model
from azureml.core.runconfig import RunConfiguration
from azureml.exceptions import ExperimentExecutionException

from . import _automlbase, _constants_azureml, constants
from ._automl_settings import _AutoMLSettings
from ._console_interface import RemoteConsoleInterface
from .utilities import friendly_http_exception

# Task: 287629 Remove when Mix-in available
RUN_STARTING = "Starting"
RUN_PREPARING = "Preparing"
RUN_RUNNING = "Running"
RUN_FINALIZING = "Finalizing"
RUN_CANCELREQUESTED = "CancelRequested"
STATUS = 'status'


class AutoMLRun(Run):
    """
    AutoMLRun has information of the experiment runs that correspond to the AutoML run.

    This class can be used to manage, check status, and retrieve run details
    once a AutoML run is submitted.

    :param experiment: The experiment associated to the run.
    :type experiement: azureml.core.Experiment
    :param run_id: The id associated to the run.
    :type run_id: str
    """

    local_model_path = "model.pkl"

    def __init__(self, experiment, run_id, **kwargs):
        """
        Initializes an AutoML run

        :param experiment: The experiment associated to the run.
        :type experiement: azureml.core.Experiment
        :param run_id: The id associated to the run.
        :type run_id: str
        """
        try:
            host = kwargs.pop('host', None)
            super(AutoMLRun, self).__init__(experiment=experiment, run_id=run_id, **kwargs)
        except HttpOperationError as e:
            self._log_traceback(e)
            friendly_http_exception(e, _constants_azureml.API.InstantiateRun)

        self._jasmine_client = JasmineClient.create(self.experiment.workspace,
                                                    self.experiment.name,
                                                    host=host)

    @property
    def run_id(self):
        """
        Returns run id of the current run.

        :return: run id of the current run.
        :rtype: str
        """
        return self._run_id

    def cancel(self):
        """
        Cancels an AutoML run.
        Return True if the AutoML run is canceled successfully.

        :return: None
        """
        try:
            self._jasmine_client.cancel_child_run(self._run_id)
        except HttpOperationError as e:
            self._log_traceback(e)
            friendly_http_exception(e, _constants_azureml.API.CancelChildRun)
        except Exception as e:
            self._log_traceback(e)
            raise ServiceException("Failed when communicating with "
                                   "Jasmine service to cancel parent run.") from None

    def cancel_iteration(self, iteration):
        """
        Cancel a particular child run

        :param iteration: Which iteration to cancel.
        :type iteration: int
        :return: None
        """
        try:
            self._jasmine_client.cancel_child_run(
                self._run_id + '_' + str(iteration))
        except HttpOperationError as e:
            self._log_traceback(e)
            friendly_http_exception(e, _constants_azureml.API.CancelChildRun)
        except Exception as e:
            self._log_traceback(e)
            raise ServiceException("Failed when communicating with "
                                   "Jasmine service to cancel iteration: {0}.".format(iteration)) from None

    def continue_experiment(
            self,
            iterations=None,
            data_script=None,
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
            show_output=False):
        """
        Continue an existing AutoML Experiment

        :param iterations: How many additional iterations to run for this experiment.
        :type iterations: int
        :param data_script: File path to the script containing get_data().
        :type data_script: str
        :param X: Training features.
        :type X: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
        :param y: Training labels.
        :type y: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
        :param sample_weight: Sample weights for training data.
        :type sample_weight: pandas.DataFrame pr numpy.ndarray or azureml.dataprep.Dataflow
        :param X_valid: validation features.
        :type X_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
        :param y_valid: validation labels.
        :type y_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
        :param sample_weight_valid: validation set sample weights.
        :type sample_weight_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
        :param data: Training features and label.
        :type data: pandas.DataFrame
        :param label: Label column in data.
        :type label: str
        :param columns: whitelist of columns in data to use as features.
        :type columns: list(str)
        :param cv_splits_indices:
            Indices where to split training data for cross validation.
            Each row is a separate cross fold and within each crossfold, provide 2 arrays,
            the first with the indices for samples to use for training data and the second
            with the indices to use for validation data. i.e [[t1, v1], [t2, v2], ...]
            where t1 is the training indices for the first cross fold and v1 is the validation
            indices for the first cross fold.
        :type cv_splits_indices: numpy.ndarray
        :param show_output: Flag whether to print output to console.
        :type show_output: bool
        :return: AutoML parent run.
        :rtype: azureml.train.automl.run.AutoMLRun
        """
        if not isinstance(iterations, int) and iterations is not None:
            raise TypeError("iterations expected 'int' or 'None' received '{0}'".format(type(iterations)))

        properties = self.get_properties()
        if 'AMLSettingsJsonString' not in properties:
            raise Exception(
                'Previous run failed before starting any iterations. Please submit a new experiment.')

        automl_settings = _AutoMLSettings(
            experiment=self.experiment,
            **json.loads(properties['AMLSettingsJsonString']))
        tags = self.get_tags()

        if iterations is None:
            if 'iterations' in tags:
                iterations = int(tags['iterations'])
            else:
                iterations = int(automl_settings.iterations)
            automl_settings.iterations = iterations
            self.tag('iterations', str(automl_settings.iterations))
        else:
            run_iters = len(list(self.get_children(_rehydrate_runs=False)))
            automl_settings.iterations = iterations + run_iters
            self.tag('iterations', str(automl_settings.iterations))

        automl_settings.data_script = data_script
        if automl_settings.metric_operation is None:
            automl_settings.metric_operation = minimize_or_maximize(
                automl_settings.primary_metric)
        automl = _automlbase._AutoMLBase(
            experiment=self.experiment, **automl_settings.__dict__)
        automl.parent_run_id = self._run_id
        automl.current_run = self

        if automl_settings.compute_target is not None and automl_settings.compute_target != 'local':
            try:
                self._jasmine_client.continue_remote_run(self.id, automl_settings.iterations)
            except Exception as e:
                self._log_traceback(e)
                raise e
            return self

        if 'best_score' in tags:
            best_score = tags['best_score']
        else:
            pass
            best_run, _ = self.get_output()
            best_score = best_run.get_metrics()[automl_settings.primary_metric]

        automl._score_best = best_score
        automl._score_max = best_score
        automl._score_min = best_score

        # recreate run config object from folder
        run_config = RunConfiguration.load(path=automl.automl_settings.path,
                                           name=automl.automl_settings.compute_target)

        return automl.fit(
            run_configuration=run_config,
            X=X,
            y=y,
            sample_weight=sample_weight,
            X_valid=X_valid,
            y_valid=y_valid,
            sample_weight_valid=sample_weight_valid,
            data=data,
            label=label,
            columns=columns,
            cv_splits_indices=cv_splits_indices,
            show_output=show_output,
            existing_run=True)

    def get_output(self, iteration=None, metric=None):
        """
        Returns the best pipeline that has already been tested. If no input is provided get_output
        will return the best pipeline according to the primary metric.

        :param iteration: The iteration number of the correspond pipeline spec and fitted model to return.
        :type iteration: int
        :param metric: The metric to use to return the best pipeline spec and fitted model to return.
        :type metric: str
        :return: The best pipeline spec, the corresponding fitted model.
        :rtype: azureml.train.automl.run.AutoMLRun, Model
        """
        if iteration is not None and metric is not None:
            raise ValueError(
                'Cannot spcify both metric and iteration to register.')

        model_name = constants.MODEL_PATH
        model_local = self.local_model_path

        properties = self.get_properties()

        automl_settings = _AutoMLSettings(
            experiment=self.experiment,
            **json.loads(properties['AMLSettingsJsonString']))

        if metric is None:
            metric = automl_settings.primary_metric

        if metric in constants.Metric.CLASSIFICATION_SET:
            objective = constants.MetricObjective.Classification[metric]
        elif metric in constants.Metric.REGRESSION_SET:
            objective = constants.MetricObjective.Regression[metric]
        else:
            raise Exception("Invalid metric.")

        if iteration is not None:
            parent_tags = self.get_tags()
            if 'iterations' in parent_tags:
                total_runs = int(parent_tags['iterations'])
            else:
                total_runs = int(self.get_properties()['num_iterations'])

            if not isinstance(iteration, str) and iteration >= total_runs:
                raise ValueError("Invalid iteration. Run {0} has {1} iterations."
                                 .format(self.run_id, total_runs))

            try:
                curr_run = Run(experiment=self.experiment,
                               run_id=self.run_id + '_' + str(iteration))
                if curr_run.get_status() != constants.Status.Completed:
                    raise ValueError("Run {0} is still in progress.".format(iteration))
            except HttpOperationError as e:
                if 'ResourceNotFoundException' in e.message:
                    raise ValueError("Run {0} has not started yet.".format(iteration))
                else:
                    raise
        else:
            children = self.get_children(_rehydrate_runs=False)
            curr_run = None
            best_score = None
            comp = _get_max_min_comparator(objective)
            for child in children:
                try:
                    if child._run_dto[STATUS] == constants.Status.Completed:
                        candidate_score = child.get_metrics()[metric]
                        if not np.isnan(candidate_score):
                            if best_score is None:
                                best_score = candidate_score
                                curr_run = child
                            else:
                                new_score = comp(best_score, candidate_score)
                                if new_score != best_score:
                                    best_score = new_score
                                    curr_run = child
                except Exception:
                    continue

            if curr_run is None:
                raise Exception("Could not find model with valid score for metric '{0}'".format(metric))

        curr_run.download_file(name=model_name, output_file_path=model_local)

        # back-compat old models
        from automl.client.core.common import model_wrappers
        import sys
        sys.modules['azureml.train.automl.model_wrappers'] = model_wrappers

        with open(model_local, "rb") as model_file:
            fitted_model = pickle.load(model_file)
        return curr_run, fitted_model

    def summary(self):
        """
        Get a table containing a summary of algorithms attempted and their scores.

        :return: Pandas DataFrame containing AutoML model statistics.
        :rtype: pandas.DataFrame
        """
        children = self.get_children(_rehydrate_runs=False)
        properties = self.get_properties()

        automl_settings = json.loads(properties['AMLSettingsJsonString'])
        primary_metric = properties['primary_metric']
        objective = automl_settings['metric_operation']

        algo_count = {}
        best_score = {}
        for child_run in children:
            metrics = child_run.get_metrics()
            properties = child_run.get_properties()
            score = constants.Defaults.DEFAULT_PIPELINE_SCORE
            if primary_metric in metrics:
                score = metrics[primary_metric]
            if 'run_algorithm' in properties:
                algo = properties['run_algorithm']
            else:
                algo = 'Failed'
            if algo not in algo_count:
                algo_count[algo] = 1
                best_score[algo] = score
            else:
                algo_count[algo] = algo_count[algo] + 1
                if objective == constants.OptimizerObjectives.MINIMIZE:
                    if score < best_score[algo] or np.isnan(best_score[algo]):
                        best_score[algo] = score
                else:
                    if score > best_score[algo] or np.isnan(best_score[algo]):
                        best_score[algo] = score

        algo_comp = pd.DataFrame(columns=['Algorithm', 'Count', 'Best Score'])
        for key in algo_count:
            algo_comp.loc[len(algo_comp)] = [
                key, algo_count[key], best_score[key]]
        return algo_comp

    def register_model(self, description=None, tags=None, iteration=None, metric=None):
        """
        Register the model with AzureML ACI service.

        :param description: Description for the model being deployed.
        :type description: str
        :param tags: Tags for the model being deployed.
        :type tags: dict
        :param iteration: Override for which model to deploy. Deploys the model for a given iteration.
        :type iteration: int
        :param metric: Override for which model to deploy. Deploys the best model for a different metric.
        :type metric: str
        :return: The registered model object.
        :rtype: Model
        """
        self.get_output(iteration, metric)

        self.model_id = self.run_id.replace('_', '').replace('-', '')[:15]
        if iteration is not None:
            self.model_id += str(iteration)
        elif metric is not None:
            self.model_id += metric
        else:
            self.model_id += 'best'
        self.model_id = self.model_id.replace('_', '')[:29]

        return self._call_register(tags, description)

    def _call_register(self, tags, description):
        return Model.register(model_path=self.local_model_path,
                              model_name=self.model_id,
                              tags=tags,
                              description=description,
                              workspace=self.experiment.workspace)

    def retry(self):
        """Return True if the AutoML run is retried successfully."""
        raise NotImplementedError

    def pause(self):
        """Return True if the AutoML run is paused successfully."""
        raise NotImplementedError

    def resume(self):
        """Return True if the AutoML run is resumed successfully."""
        raise NotImplementedError

    def _log_traceback(self, exception):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error("Line {} in {}".format(exc_tb.tb_lineno, fname))
        logging.error(exception)

    def get_run_sdk_dependencies(
        self,
        iteration=None,
        check_versions=True,
        **kwargs
    ):
        """
        Gets the SDK run dependencies for a given run.

        :param iteration:
            The iteration number of the fitted run that going to be retrieved. If None, retrieve the
            parent environment.
        :type iteration: int
        :param check_versions: If True, check the versions with current env. If False, pass.
        :type check_versions: bool
        :return: The dict of dependencies from those retrieved from RunHistory.
        :rtype: dict
        """
        console_output = sys.stdout
        properties = self.get_properties()
        if iteration is not None:
            if iteration < 0:
                raise Exception('Iteration number must be greater than or equal to 0.')
        try:
            if iteration is None:
                console_output.write("Iteration number is not passed, retrieve the environment for the parent run.\n")
            else:
                curr_run = AutoMLRun(experiment=self.experiment,
                                     run_id=self.run_id + '_' + str(iteration))
                properties = curr_run.get_properties()
            dependencies_versions = json.loads(properties['dependencies_versions'])
            logging.info('All the dependencies and the corresponding versions in the environment are:')
            logging.info(
                ';'.join(
                    [
                        '{}=={}'.format(d, dependencies_versions[d]) for d in sorted(dependencies_versions.keys())
                    ]
                )
            )
        except Exception:
            logging.warning('No dependencies information found in the RunHistory.')
            return dict()

        sdk_dependencies = get_sdk_dependencies(
            all_dependencies_versions=dependencies_versions,
            logger=logging,
            **kwargs
        )

        if check_versions:
            current_dependencies = _all_dependencies()
            sdk_mismatch, sdk_missing, other_mismatch, other_missing = _check_dependencies_versions(
                sdk_dependencies, current_dependencies
            )

            if len(sdk_mismatch) == 0 and len(sdk_missing) == 0:
                message = 'No issues found in the SDK package versions.\n'
                console_output.write(message)
                logging.info(message)

            if len(sdk_mismatch) > 0:
                logging.warning('The version of the SDK does not match the version the model was trained on.')
                logging.warning('The consistency in the result may not be guranteed.')
                logging.warning(
                    '\n'.join(
                        [
                            'Package:{}, training version:{}, current version:{}'.format(
                                d, sdk_dependencies[d], current_dependencies[d]
                            )
                            for d in sorted(sdk_mismatch)
                        ]
                    )
                )

            if len(sdk_missing) > 0:
                logging.warning('Below SDKs were used for model training but missing in current environment:')
                logging.warning(
                    '\n'.join(
                        [
                            'Package:{}, training version:{}'.format(d, sdk_dependencies[d])
                            for d in sorted(sdk_missing)
                        ]
                    )
                )

        return sdk_dependencies

    # Task: 287629 Remove when Mix-in available
    def wait_for_completion(self, show_output=False, wait_post_processing=False):
        """
        Waits for the completion of this run.
        Returns the status object after the wait.

        :param show_output: show_output=True shows the run output on sys.stdout.
        :type show_output: bool
        :param wait_post_processing:
            wait_post_processing=True waits for the post processing to
            complete after the run completes.
        :type wait_post_processing: bool
        :return: The status object.
        :rtype: dict
        """

        if show_output:
            try:
                self._stream_run_output(file_handle=sys.stdout)
            except KeyboardInterrupt:
                error_message = "The output streaming for the run interrupted.\n" \
                                "But the run is still executing on the compute target."

                raise ExperimentExecutionException(error_message)
        else:
            running_states = [RUN_STARTING, RUN_PREPARING, RUN_RUNNING]
            if wait_post_processing:
                running_states.append(RUN_FINALIZING)
                running_states.append(RUN_CANCELREQUESTED)

            current_status = None
            while current_status is None or current_status in running_states:
                time.sleep(1)
                current_status = self.get_status()

        return self.get_details()

    def _stream_run_output(self, file_handle=sys.stdout):
        """
        Streams the experiment run output to the specified file handle.
        By default the the file handle points to stdout.

        :param file_handle: A file handle to stream the output to.
        :type file_handle: file
        :return:
        """
        properties = self.get_properties()
        tags = self.get_tags()
        primary_metric = properties['primary_metric']
        if 'iterations' in tags:
            iterations = tags['iterations']
        else:
            iterations = properties['num_iterations']
        remote_printer = RemoteConsoleInterface(file_handle, None)
        remote_printer.print(
            self,
            primary_metric,
            iterations)

        file_handle.write("\n")
        file_handle.write("Execution Summary\n")
        file_handle.write("=================\n")
        file_handle.write("RunId: {}\n".format(self.id))
        file_handle.write("\n")
        file_handle.flush()
