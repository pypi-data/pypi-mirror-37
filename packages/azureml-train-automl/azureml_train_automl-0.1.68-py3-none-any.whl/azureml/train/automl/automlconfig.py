# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""AutoML configuration for submitting an AutoML experiment to AzureML."""
import inspect
import logging
import os
from functools import reduce

from azureml.core._experiment_method import experiment_method
from azureml.core.experiment import Experiment
from azureml.core.runconfig import RunConfiguration

from . import constants
from . import _dataprep_utilities

from ._automlbase import _AutoMLBase
from ._automlclassifier import _AutoMLClassifier
from ._automlregressor import _AutoMLRegressor


def _automl_static_submit(automl_config_object,
                          workspace,
                          experiment_name,
                          **kwargs):
    """
    Start AutoML execution with the given config on the given workspace.

    :param automl_config_object:
    :param workspace:
    :param experiment_name:
    :param kwargs:
    :return:
    """
    automl_config_object._validate_config_settings()
    automl_config_object._get_remove_fit_params()

    experiment = Experiment(workspace, experiment_name)

    show_output = kwargs.get('show_output', None)

    settings = automl_config_object.user_settings

    if automl_config_object._task_type == constants.Tasks.CLASSIFICATION:
        automl_estimator = _AutoMLClassifier(experiment, **settings)
    else:
        automl_estimator = _AutoMLRegressor(experiment, **settings)

    return automl_estimator.fit(**automl_config_object.fit_params,
                                show_output=show_output)


class AutoMLConfig(object):
    """
    AutoML configuration for submitting an AutoML experiment to AzureML. This configuration object
    contains persists the parameters for configuring the AutoML experiment as well as the data to be used
    at run time. This configuration is directly submitted as an AzureML experiment as follows:

    .. code-block:: python

        >>> experiment.submit(AutoMLConfig)


    :param task: \'classification\' or \'regression\' depending on what kind of ML problem to solve.
    :type task: str or azureml.train.automl.constants.Tasks
    :param path: Full path to the AzureML project folder.
    :type path: str
    :param iterations:
        Total number of different algorithm and parameter combinations
        to test during an AutoML experiment.
    :type iterations: int
    :param data_script: File path to the user authored script containing get_data() function.
    :type data_script: str
    :param primary_metric:
        The metric that AutoML will optimize for model selection. AutoML collects more metrics
        than it can optimize. Please consult azureml.train.automl.constants.Metric.CLASSIFICATION_PRIMARY_SET for
        valid metrics for a classification task and azureml.train.automl.constants.Metric.REGRESSION_PRIMARY_SET for
        valid metrics for a regression task.
    :type primary_metric: str or azureml.train.automl.constants.Metric
    :param compute_target: The AzureML compute to run the AutoML experiment on.
    :type compute_target: azureml.core.compute.AbstractComputeTarget
    :param X: The training features to use when fitting pipelines during AutoML experiment.
    :type X: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param y: Training labels to use when fitting pipelines during AutoML experiment.
    :type y: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param sample_weight:
        The weight to give to each training sample when running fitting pipelines,
        each row should correspond to a row in X and y data.
    :type sample_weight: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param X_valid: validation features to use when fitting pipelines during AutoML experiment.
    :type X_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param y_valid: validation labels to use when fitting pipelines during AutoML experiment.
    :type y_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param sample_weight_valid:
        The weight to give to each validation sample when running scoring pipelines,
        each row should correspond to a row in X and y data.
    :type sample_weight_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param cv_splits_indices:
        Indices where to split training data for cross validation.
        Each row is a separate cross fold and within each crossfold, provide 2 arrays, t
        he first with the indices for samples to use for training data and the second with the indices to
        use for validation data. i.e [[t1, v1], [t2, v2], ...] where t1 is the training indices for the first cross
        fold and v1 is the validation indices for the first cross fold.
    :type cv_splits_indices: numpy.ndarray
    :param validation_size:
        What percent of the data to hold out for validation when user validation data
        is not specified.
    :type validation_size: float
    :param n_cross_validations: How many cross validations to perform when user validation data is not specified.
    :type n_cross_validations: int
    :param y_min: Minimum value of y for a regression experiment.
    :type y_min: float
    :param y_max: Maximum value of y for a regression experiment.
    :type y_max: float
    :param num_classes: Number of classes in the label data for a classification experiment.
    :type num_classes: int
    :param preprocess:
        Flag whether AutoML should preprocess your data for you such as handling missing data, text
        data and other common feature extraction. Note: If input data is Sparse you cannot use preprocess as True.
    :type preprocess: bool
    :param lag_length: How many rows of historical data to include when preprocessing time series data.
    :type lag_length: int
    :param max_cores_per_iteration: Maximum number of threads to use for a given training iteration.
    :type max_cores_per_iteration: int
    :param max_time_sec: Maximum time in seconds that each iteration can run for before it terminates.
    :type max_time_sec: int
    :param mem_in_mb: Maximum memory usage that each iteration can run for before it terminates.
    :type mem_in_mb: int
    :param enforce_time_on_windows:
        flag to enforce time limit on model training at each iteration under windows.
        If running from a python script file (.py) please refer to the documentation for allowing resource limits
        on windows.
    :type enforce_time_on_windows: bool
    :param exit_time_sec:
        Maximum amount of time that all iterations combined can take before the
        experiment terminates.
    :type exit_time_sec: int
    :param exit_score: Target score for experiment. Experiment will terminate after this score is reached.
    :type exit_score: int
    :param blacklist_algos: List of algorithms to ignore for AutoML experiment.
    :type blacklist_algos: list(str) or list(azureml.train.automl.constants.SupportedAlgorithms)
    :param exclude_nan_labels: Flag whether to exclude rows with NaN values in the label.
    :type exclude_nan_labels: bool
    :param auto_blacklist:
        Flag whether AutoML should try to automatically exclude algorithms
        that it thinks won't perform well or may take a disproportionally long time to train.
    :type auto_blacklist: bool
    :param verbosity: Verbosity level for AutoML log file.
    :type verbosity: int
    :param debug_log: File path to AutoML logs.
    :type debug_log: str
    """
    @experiment_method(submit_function=_automl_static_submit)
    def __init__(self,
                 task,
                 path=None,
                 iterations=100,
                 data_script=None,
                 primary_metric=None,
                 compute_target=None,
                 X=None,
                 y=None,
                 sample_weight=None,
                 X_valid=None,
                 y_valid=None,
                 sample_weight_valid=None,
                 cv_splits_indices=None,
                 validation_size=None,
                 n_cross_validations=None,
                 y_min=None,
                 y_max=None,
                 num_classes=None,
                 preprocess=False,
                 lag_length=0,
                 max_cores_per_iteration=1,
                 concurrent_iterations=1,
                 max_time_sec=None,
                 mem_in_mb=None,
                 enforce_time_on_windows=(os.name == 'nt'),
                 exit_time_sec=None,
                 exit_score=None,
                 blacklist_algos=None,
                 auto_blacklist=True,
                 exclude_nan_labels=True,
                 verbosity=logging.INFO,
                 **kwargs):
        """
        Constructor for the class.

        :param task: \'classification\' or \'regression\' depending on what kind of ML problem to solve.
        :type task: str or azureml.train.automl.constants.Tasks
        :param path: Full path to the AzureML project folder.
        :type path: str
        :param iterations:
            Total number of different algorithm and parameter combinations
            to test during an AutoML experiment.
        :type iterations: int
        :param data_script: File path to the user authored script containing get_data() function.
        :type data_script: str
        :param primary_metric:
            The metric that AutoML will optimize for model selection. AutoML collects more metrics
            than it can optimize. Please consult azureml.train.automl.constants.Metric.CLASSIFICATION_PRIMARY_SET for
            valid metrics for a classification task and azureml.train.automl.constants.Metric.REGRESSION_PRIMARY_SET
            for valid metrics for a regression task.
        :type primary_metric: str or azureml.train.automl.constants.Metric
        :param compute_target: The AzureML compute to run the AutoML experiment on.
        :type compute_target: azureml.core.compute.AbstractComputeTarget
        :param X: The training features to use when fitting pipelines during AutoML experiment.
        :type X: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
        :param y: Training labels to use when fitting pipelines during AutoML experiment.
        :type y: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
        :param sample_weight:
            The weight to give to each training sample when running fitting pipelines,
            each row should correspond to a row in X and y data.
        :type sample_weight: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
        :param X_valid: validation features to use when fitting pipelines during AutoML experiment.
        :type X_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
        :param y_valid: validation labels to use when fitting pipelines during AutoML experiment.
        :type y_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
        :param sample_weight_valid:
            The weight to give to each validation sample when running scoring pipelines,
            each row should correspond to a row in X and y data.
        :type sample_weight_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
        :param cv_splits_indices:
            Indices where to split training data for cross validation.
            Each row is a separate cross fold and within each crossfold, provide 2 arrays, t
            he first with the indices for samples to use for training data and the second with the indices to
            use for validation data. i.e [[t1, v1], [t2, v2], ...] where t1 is the training indices for the first cross
            fold and v1 is the validation indices for the first cross fold.
        :type cv_splits_indices: numpy.ndarray
        :param validation_size:
            What percent of the data to hold out for validation when user validation data
            is not specified.
        :type validation_size: float
        :param n_cross_validations: How many cross validations to perform when user validation data is not specified.
        :type n_cross_validations: int
        :param y_min: Minimum value of y for a regression experiment.
        :type y_min: float
        :param y_max: Maximum value of y for a regression experiment.
        :type y_max: float
        :param num_classes: Number of classes in the label data for a classification experiment.
        :type num_classes: int
        :param preprocess:
            Flag whether AutoML should preprocess your data for you such as handling missing data, text
            data and other common feature extraction. Note: If input data is Sparse you cannot use preprocess as True.
        :type preprocess: bool
        :param lag_length: How many rows of historical data to include when preprocessing time series data.
        :type lag_length: int
        :param max_cores_per_iteration: Maximum number of threads to use for a given training iteration.
        :type max_cores_per_iteration: int
        :param max_time_sec: Maximum time in seconds that each iteration can run for before it terminates.
        :type max_time_sec: int
        :param mem_in_mb: Maximum memory usage that each iteration can run for before it terminates.
        :type mem_in_mb: int
        :param enforce_time_on_windows:
            flag to enforce time limit on model training at each iteration under windows.
            If running from a python script file (.py) please refer to the documentation for allowing resource limits
            on windows.
        :type enforce_time_on_windows: bool
        :param exit_time_sec:
            Maximum amount of time that all iterations combined can take before the
            experiment terminates.
        :type exit_time_sec: int
        :param exit_score: Target score for experiment. Experiment will terminate after this score is reached.
        :type exit_score: int
        :param blacklist_algos: List of algorithms to ignore for AutoML experiment.
        :type blacklist_algos: list(str) or list(azureml.train.automl.constants.SupportedAlgorithms)
        :param exclude_nan_labels: Flag whether to exclude rows with NaN values in the label.
        :type exclude_nan_labels: bool
        :param auto_blacklist:
            Flag whether AutoML should try to automatically exclude algorithms
            that it thinks won't perform well or may take a disproportionally long time to train.
        :type auto_blacklist: bool
        :param verbosity: Verbosity level for AutoML log file.
        :type verbosity: int
        :param debug_log: File path to AutoML logs.
        :type debug_log: str
        """
        self.user_settings = {}
        self.fit_params = {}
        self._run_configuration = None
        self._task_type = None

        if task not in [constants.Tasks.CLASSIFICATION,
                        constants.Tasks.REGRESSION]:
            raise ValueError("Invalid Task: '{0}'. Supported Tasks: "
                             "{1}".format(task, constants.Tasks.ALL))
        if task == constants.Tasks.CLASSIFICATION:
            if y_min is not None or y_max is not None:
                raise ValueError("Classification tasks do not use"
                                 "'y_min' or 'y_max'")
        else:
            if num_classes is not None:
                raise ValueError("A regression tasks do not use 'num_classes'")

        for key, value in kwargs.items():
            self.user_settings[key] = value

        self.user_settings["primary_metric"] = primary_metric
        self.user_settings["compute_target"] = compute_target
        self.user_settings['X'] = X
        self.user_settings['y'] = y
        self.user_settings['sample_weight'] = sample_weight
        self.user_settings['X_valid'] = X_valid
        self.user_settings['y_valid'] = y_valid
        self.user_settings['sample_weight_valid'] = sample_weight_valid
        self.user_settings['cv_splits_indices'] = cv_splits_indices
        self.user_settings["num_classes"] = num_classes
        self.user_settings["y_min"] = y_min
        self.user_settings["y_max"] = y_max
        self.user_settings["path"] = path
        self.user_settings["iterations"] = iterations
        self.user_settings["data_script"] = data_script
        self.user_settings["validation_size"] = validation_size
        self.user_settings["n_cross_validations"] = n_cross_validations
        self.user_settings["preprocess"] = preprocess
        self.user_settings["lag_length"] = lag_length
        self.user_settings["max_cores_per_iteration"] = max_cores_per_iteration
        self.user_settings["concurrent_iterations"] = concurrent_iterations
        self.user_settings["max_time_sec"] = max_time_sec
        self.user_settings["mem_in_mb"] = mem_in_mb
        self.user_settings["enforce_time_on_windows"] = enforce_time_on_windows
        self.user_settings["exit_time_sec"] = exit_time_sec
        self.user_settings["exit_score"] = exit_score
        self.user_settings["blacklist_algos"] = blacklist_algos
        self.user_settings["auto_blacklist"] = auto_blacklist
        self.user_settings["exclude_nan_labels"] = exclude_nan_labels
        self.user_settings["verbosity"] = verbosity

        self._task_type = task
        self._run_configuration = self.user_settings.get('run_configuration', None)

    def _get_remove_fit_params(self):
        """
        Inspects _AutoMLBase.fit() signature and builds a dictionary
        of args to be passed in from settings, using defauls as required
        and removes these params from settings

        :returns:
        """
        if not self.fit_params:
            fit_signature = inspect.signature(_AutoMLBase.fit)
            for k, v in fit_signature.parameters.items():
                # skip parameters
                if k in ['self', 'run_configuration', 'data_script', 'show_output']:
                    continue

                default_val = v.default

                # Parameter.empty is returned for any parameters without a default
                # we will require these in settings
                if default_val is inspect.Parameter.empty:
                    try:
                        self.fit_params[k] = self.user_settings.pop(k)
                    except KeyError:
                        raise ValueError("To submit an experiment you will need"
                                         " to provide a value for '{0}'".format(k))
                else:
                    self.fit_params[k] = self.user_settings.pop(k, default_val)

        # overwrite default run_config with user provided or None
        self.fit_params['run_configuration'] = self._run_configuration

    def _validate_config_settings(self):
        """
        Validates the configuration attributes
        """
        # assert we have a run_config, if not create default
        # and assume default config
        if self._run_configuration is None:
            if 'run_configuration' not in self.user_settings.keys():
                self._run_configuration = RunConfiguration()
                self._run_configuration.auto_prepare_environment = True
            elif isinstance(self.user_settings['run_configuration'], str):
                path = self.user_settings.get('path', '.')
                self._run_configuration = RunConfiguration.load(path=path,
                                                                name=self.user_settings['run_configuration'])
            else:
                self._run_configuration = self.user_settings['run_configuration']

        # ensure compute target is set
        if 'compute_target' in self.user_settings and self.user_settings['compute_target'] is not None:
            self._run_configuration.target = self.user_settings['compute_target']
            if self.user_settings['compute_target'].type == constants.ComputeTargets.BATCHAI:
                self._run_configuration.environment.docker.enabled = True
        else:
            self.user_settings['compute_target'] = self._run_configuration.target
        # remove compute target from setting
        self.user_settings.pop('run_configuration', None)

        # validate data for remote
        settings = self.user_settings
        if settings['compute_target'] != 'local':
            data_script_provided = 'data_script' in settings.keys()

            def are_dataflows_valid():
                for key in ['X', 'y', 'sample_weight', 'X_valid', 'y_valid', 'sample_weight_valid']:
                    if key not in settings.keys():
                        continue
                    value = settings[key]
                    if value is not None and not _dataprep_utilities.is_dataflow(value):
                        return False
                if 'cv_splits_indices' in settings.keys():
                    cv_splits_indices = settings['cv_splits_indices']
                    if not isinstance(cv_splits_indices, list):
                        return False
                    for split in cv_splits_indices:
                        if not _dataprep_utilities.is_dataflow(split):
                            return False
                return True

            if not data_script_provided and not are_dataflows_valid():
                raise ValueError("You must provide a 'data_script'"
                                 " or provide data with `azureml.dataprep.Dataflow` "
                                 " to create a remote run")
