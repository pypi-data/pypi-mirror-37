# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Manages settings for AutoML experiment"""
import json
import logging
import os

from automl.client.core.common.metrics import (get_default_metrics,
                                               minimize_or_maximize)

from azureml._base_sdk_common import service_discovery
from azureml.core import Experiment

from . import constants
from ._logging import get_logger
from .utilities import _get_primary_metrics


class _AutoMLSettings(object):
    """
    Persists and validates settings for an AutoML experiment
    """

    def __init__(self,
                 experiment,
                 path=None,
                 iterations=100,
                 data_script=None,
                 primary_metric=None,
                 task_type=None,
                 compute_target=None,
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
                 enforce_time_on_windows=None,
                 exit_time_sec=None,
                 exit_score=None,
                 blacklist_algos=None,
                 auto_blacklist=True,
                 exclude_nan_labels=True,
                 verbosity=logging.INFO,
                 debug_log='automl.log',
                 debug_flag=None,
                 enable_ensembling=False,
                 ensemble_iterations=1,
                 **kwargs):
        """
        Class to manage settings used by AutoML components
        :param experiment: The azureml.core experiment
        :param path: Full path to the project folder
        :param iterations: Number of different pipelines to test
        :param data_script: File path to the script containing get_data()
        :param primary_metric: The metric that you want to optimize.
        :param task_type: Field describing whether this will be a classification or regression experiment
        :param compute_target: The AzureML compute to run the AutoML experiment on
        :param validation_size: What percent of the data to hold out for validation
        :param n_cross_validations: How many cross validations to perform
        :param y_min: Minimum value of y for a regression experiment
        :param y_max: Maximum value of y for a regression experiment
        :param num_classes: Number of classes in the label data
        :param preprocess: Flag whether AutoML should preprocess your data for you
        :param lag_length: How many rows to lag data when preprocessing time series data
        :param max_cores_per_iteration: Maximum number of threads to use for a given iteration
        :param max_time_sec: Maximum time in seconds that each iteration before it terminates
        :param mem_in_mb: Maximum memory usage of each iteration before it terminates
        :param enforce_time_on_windows: flag to enforce time limit on model training at each iteration under windows.
        :param exit_time_sec: Maximum amount of time that all iterations combined can take
        :param exit_score: Target score for experiment. Experiment will terminate after this score is reached.
        :param blacklist_algos: List of algorithms to ignore for AutoML experiment
        :param exclude_nan_labels: Flag whether to exclude rows with NaN values in the label
        :param auto_blacklist: Flag whether AutoML should try to exclude algorithms
            that it thinks won't perform well.
        :param verbosity: Verbosity level for AutoML log file
        :param debug_log: File path to AutoML logs
        :param enable_ensembling: Flag to enable/disable an extra iteration for model ensembling
        :param ensemble_iterations: Number of models to consider for the ensemble generation
        :param kwargs:
        """

        if experiment is None:
            self.name = None
            self.path = None
            workspace = None
            self.subscription_id = None
            self.resource_group = None
            self.workspace_name = None
        else:
            # This is used in the remote case values are populated through
            # AMLSettings
            self.name = experiment.name
            self.path = path
            workspace = experiment.workspace
            self.subscription_id = workspace.subscription_id
            self.resource_group = workspace.resource_group
            self.workspace_name = workspace.name

        self.iterations = iterations
        self.primary_metric = primary_metric
        self.data_script = data_script

        self.compute_target = compute_target
        self.task_type = task_type

        # TODO remove this once Miro/AutoML common code can handle None
        if validation_size is None:
            self.validation_size = 0.0
        else:
            self.validation_size = validation_size
        self.n_cross_validations = n_cross_validations

        self.y_min = y_min
        self.y_max = y_max

        self.num_classes = num_classes

        self.preprocess = preprocess
        self.lag_length = lag_length

        self.max_cores_per_iteration = max_cores_per_iteration
        self.concurrent_iterations = concurrent_iterations
        self.max_time_sec = max_time_sec
        self.mem_in_mb = mem_in_mb
        self.enforce_time_on_windows = enforce_time_on_windows
        self.exit_time_sec = exit_time_sec
        self.exit_score = exit_score

        self.blacklist_algos = blacklist_algos
        self.auto_blacklist = auto_blacklist
        self.blacklist_samples_reached = False
        self.exclude_nan_labels = exclude_nan_labels

        self.verbosity = verbosity
        self.debug_log = debug_log
        self.show_warnings = False
        self.service_url = None
        self.sdk_url = None
        self.sdk_packages = None

        # telemetry settings
        self.telemetry_verbosity = logging.getLevelName(logging.NOTSET)
        self.send_telemetry = False

        if debug_flag:
            if 'service_url' in debug_flag:
                self.service_url = debug_flag['service_url']
            if 'show_warnings' in debug_flag:
                self.show_warnings = debug_flag['show_warnings']
            if 'sdk_url' in debug_flag:
                self.sdk_url = debug_flag['sdk_url']
            if 'sdk_packages' in debug_flag:
                self.sdk_packages = debug_flag['sdk_packages']

        if self.service_url is None and workspace is not None:
            self.service_url = service_discovery.get_history_service_url(workspace._auth_object,
                                                                         workspace.get_details()['id'])
        # Deprecated param
        self.metrics = None

        self.enable_ensembling = enable_ensembling
        self.ensemble_iterations = ensemble_iterations

        self._verify_settings()

        # Settings that need to be set after verification
        if self.task_type is not None and self.primary_metric is not None:
            self.metric_operation = minimize_or_maximize(
                task=self.task_type, metric=self.primary_metric)
        else:
            self.metric_operation = None

        for key, value in kwargs.items():
            if key not in self.__dict__.keys():
                logging.warning(
                    "Received unrecognized parameter: {0} {1}".format(
                        key, value))
            setattr(self, key, value)

    def _verify_settings(self):
        """
        Verify that input automl_settings are sensible
        :return: None
        """
        if self.n_cross_validations is not None and self.validation_size is not None:
            if not (self.n_cross_validations > 0) and not (
                    self.validation_size > 0.0):
                logging.warning("Neither n_cross_validations nor validation_size specified. "
                                "You will need to either pass custom validation data or cv_split_indices to "
                                "the submit(), fit(), or get_data() methods.")

        if self.validation_size is not None:
            if self.validation_size > 1.0 or self.validation_size < 0.0:
                raise ValueError(
                    "validation_size parameter must be between 0 and 1 when specified.")

        if self.n_cross_validations is not None:
            if self.n_cross_validations == 1 or self.n_cross_validations < 0:
                raise ValueError(
                    "n_cross_validations must be greater than or equal to 2 when specified.")

        if self.iterations > constants.MAX_ITERATIONS:
            raise ValueError(
                "Number of iterations cannot be larger than {0}.".format(
                    constants.MAX_ITERATIONS))

        if self.primary_metric is None:
            if self.task_type is constants.Tasks.CLASSIFICATION:
                self.primary_metric = constants.Metric.Accuracy
            elif self.task_type is constants.Tasks.REGRESSION:
                self.primary_metric = constants.Metric.Spearman
        else:
            if self.task_type is not None:
                if self.primary_metric not in _get_primary_metrics(
                        self.task_type):
                    raise ValueError("Invalid primary metric specified for {0}. Please use on of: {1}".format(
                        self.task_type, _get_primary_metrics(self.task_type)))
            else:
                if self.primary_metric in constants.Metric.REGRESSION_PRIMARY_SET:
                    self.task_type = constants.Tasks.REGRESSION
                elif self.primary_metric in constants.Metric.CLASSIFICATION_PRIMARY_SET:
                    self.task_type = constants.Tasks.CLASSIFICATION
                else:
                    raise ValueError("Invalid primary metric specified. Please use one of {0} for classification or "
                                     "{1} for regression.".format(constants.Metric.CLASSIFICATION_PRIMARY_SET,
                                                                  constants.Metric.REGRESSION_PRIMARY_SET))

        if self.enforce_time_on_windows:
            try:
                import psutil
            except Exception:
                self.enforce_time_on_windows = False
                logging.warning("psutil not found, disabling enforce_time_on_windows. "
                                "enforce_time_on_windows requires psutil library to be installed.")
        else:
            if os.name == 'nt':
                try:
                    import psutil
                    self.enforce_time_on_windows = True
                except Exception:
                    pass

        if self.enable_ensembling and self.ensemble_iterations < 1:
            raise ValueError("When ensembling is enabled, the ensemble_iterations setting can't be less than 1")

        if self.enable_ensembling and self.ensemble_iterations > self.iterations:
            raise ValueError(
                "When ensembling is enabled, the ensemble_iterations setting can't be greater than \
                the total number of iterations".format(self.iterations))

    @staticmethod
    def from_string_or_dict(input, experiment=None):
        if isinstance(input, str):
            input = eval(input)
        if isinstance(input, dict):
            input = _AutoMLSettings(experiment=experiment, **input)

        if isinstance(input, _AutoMLSettings):
            return input
        else:
            raise ValueError("`input` parameter is not of type string or dict")
