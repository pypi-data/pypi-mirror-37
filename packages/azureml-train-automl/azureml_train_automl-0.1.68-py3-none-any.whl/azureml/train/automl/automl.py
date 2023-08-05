# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Global methods used during an AutoML iteration for both remote and local runs."""
import json
import logging
import os
import os.path
import pickle
import sys  # noqa F401
import tempfile
import traceback

import numpy as np
import pandas as pd
import scipy
import sklearn  # noqa F401 # TODO: dynamically import these based on JOS output
from automl.client.core.common import pipeline_spec
from automl.client.core.common.datasets import ClientDatasets
from automl.client.core.common.exceptions import (DataException,
                                                  ServiceException)
from automl.client.core.common.metrics import minimize_or_maximize
from automl.client.core.common.model_wrappers import \
    TruncatedSVDWrapper  # noqa F401
from automl.client.core.common.model_wrappers import (CalibratedModel, FastICA,
                                                      LightGBMClassifier,
                                                      LightGBMRegressor,
                                                      LinearSVMWrapper,
                                                      NBWrapper, NuSVCWrapper,
                                                      SGDClassifierWrapper,
                                                      SparseNormalizer,
                                                      SVCWrapper)
from automl.client.core.common.preprocess import (DataTransformer,
                                                  LaggingTransformer)
from automl.client.core.common.resource_limits import (default_resource_limits,
                                                       safe_enforce_limits)
from automl.client.core.common.runner_legacy import ClientRunner
from automl.client.core.common.utilities import (_log_traceback,
                                                 get_sdk_dependencies,
                                                 get_value_float,
                                                 get_value_from_dict,
                                                 get_value_int)
from sklearn import (decomposition, ensemble, linear_model,  # noqa F401
                     pipeline, preprocessing)
from sklearn.metrics import precision_score, recall_score  # noqa F401
from sklearn.model_selection import cross_val_score  # noqa F401
from sklearn.pipeline import make_pipeline

from azureml.core import Experiment, Run
from azureml.telemetry import (get_telemetry_log_handler,
                               set_diagnostics_collection)
from azureml.telemetry.logging_handler import AppInsightsLoggingHandler

from . import _constants_azureml, constants
from ._automl_settings import _AutoMLSettings
from ._limit_function_call_for_win import enforce_time_limit
from ._logging import get_logger, _log_system_info
from ._systemusage_telemetry import SystemResourceUsageTelemetryFactory
from .ensemble import Ensemble
from .utilities import _validate_training_data

SOURCE_WRAPPER_MODULE = 'automl.client.core.common.model_wrappers'


def _get_problem_info(X, y, task_type):
    dataset = ClientDatasets()
    dataset.parse_data("parse", X, y, task_type, init_all_stats=False)
    problem_info = dataset.get_problem_info()
    return problem_info


def set_problem_info(X, y, task_type, current_run=None, workspace=None,
                     experiment_name=None, run_id=None, preprocess=False,
                     lag_length=0):
    """
    Set statistics about user data.

    :param X: The training features to use when fitting pipelines during AutoML experiment.
    :type X: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param y: Training labels to use when fitting pipelines during AutoML experiment.
    :type y: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param task: \'classification\' or \'regression\' depending on what kind of ML problem to solve.
    :type task: str or azureml.train.automl.constants.Tasks
    :param current_run: The AutoMLRun to set the info for.
    :type current_run: azureml.core.run.Run
    :param workspace: AzureML workspace containing this run.
    :type workspace: azureml.core.workspace.Workspace
    :param experiment_name: The experiemnt name.
    :type experiment_name: str
    :param run_id: ID of the run to set the info for.
    :type run_id: str
    :param preprocess: Flag whether to preprocess the data.
    :type preprocess: bool
    :param lag_length: How much to lag the features by for Lagging preprocessor.
    :type lag_length: int
    :return: None
    """
    x_raw_column_names = None
    if isinstance(X, pd.DataFrame):
        x_raw_column_names = X.columns.values
    if preprocess and not scipy.sparse.issparse(X):
        _, _, X, _ = _transform_data(None, X, y, None, task_type,
                                     x_raw_column_names, lag_length)

    problem_info_dict = {
        "dataset_num_categorical": 0,
        "dataset_classes": len(np.unique(y)),
        "dataset_features": X.shape[1],
        "dataset_samples": X.shape[0],
        "is_sparse": scipy.sparse.issparse(X)
    }
    problem_info_str = json.dumps(problem_info_dict)
    if current_run is None:
        experiment = Experiment(workspace, experiment_name)
        current_run = Run(experiment, run_id)
    current_run.add_properties(
        {_constants_azureml.Properties.PROBLEM_INFO: problem_info_str})


def _transform_data(logger, X, y, X_valid, task_type, x_raw_column_names,
                    lag_length):
    """
    Apply data transfomers for input data

    :param logger: Logger for intermediate messages
    :param X_valid: Validation data
    :param task_type: Validation labels
    :param x_raw_column_names: Column headers for the data
    :param lag_length: Length by which to lag the data
    :return:
    """
    if logger:
        logger.info("Pre-processing user data")

    transformer, lag_transformer = None, None
    try:
        X = _add_raw_column_names_to_X(x_raw_column_names, X)
        transformer, X = _get_transformer_x(X, y, task_type, logger)
    except ValueError:
        raise Exception(
            "Cannot preprocess training data. Run after processing manually.")

    if X_valid is not None:
        try:
            X_valid = _add_raw_column_names_to_X(x_raw_column_names, X_valid)
            X_valid = transformer.transform(X_valid)
        except ValueError:
            raise Exception(
                "Cannot preprocess validation data. Run after processing manually.")

    # todo can probably be moved to a helper
    if lag_length > 0:
        lag_transformer = LaggingTransformer(lag_length)
        X = lag_transformer.fit_transform(X)
        if X_valid is not None:
            X_valid = lag_transformer.fit_transform(X_valid)
        if logger:
            logger.info(
                "lagging transformer is enabled with length {}.".format(lag_length))

    if isinstance(X, pd.DataFrame):
        # X should be a numpy array
        X = X.values
    return transformer, lag_transformer, X, X_valid


def fit_pipeline(pipeline_script,
                 automl_settings,
                 run_id,
                 X,
                 y,
                 sample_weight=None,
                 X_valid=None,
                 y_valid=None,
                 sample_weight_valid=None,
                 cv_splits_indices=None,
                 fit_iteration_parameters_dict=None,
                 experiment=None,
                 iteration=None,
                 pipeline_id=None,
                 experiment_id=None,
                 score_min=None,
                 score_max=None,
                 remote=True,
                 logger=None,
                 project=None):
    """
    Runs a single iteration of an AutoML experiment. This method is automatically called during a regular AutoML
    experiment. fit_pipeline will evaluate the pipeline for this iteration, fit the pipeline with the provided data,
    calculate the various metrics relevant for this experiment, and log all the results in the specified AzureML Run's
    history.

    :param pipeline_script: serialized Pipeline returned from the server.
    :type pipeline_script: str
    :param automl_settings: User settings specified when creating AutoMLConfig.
    :type automl_settings: str or dict
    :param run_id: AzureML Child Run id for this fit.
    :type run_id: str
    :param X: Input training data.
    :type X: numpy.ndarray or pandas.DataFrame
    :param y: Input training labels.
    :type y: numpy.ndarray or pandas.DataFrame
    :param sample_weight: Sample weights for training data.
    :type sample_weight: numpy.ndarray or pandas.DataFrame
    :param X_valid: validation data.
    :type X_valid: numpy.ndarray or pandas.DataFrame
    :param y_valid: validation labels.
    :type y_valid: numpy.ndarray or pandas.DataFrame
    :param sample_weight_valid: validation set sample weights.
    :type sample_weight_valid: numpy.ndarray or pandas.DataFrame
    :param cv_splits_indices: Custom indices by which to split the data when running cross validation.
    :type cv_splits_indices: numpy.ndarray or pandas.DataFrame
    :param experiment: The azureml.core experiment.
    :type experiment: azureml.core.experiment.Experiment
    :param iteration: Current iteration being executed.
    :type iteration: int
    :param pipeline_id: Hash Id of current pipeline being evaluated.
    :type pipeline_id: str
    :param experiment_id: Id of the current experiment.
    :type experiment_id: str
    :param score_min: current min score for the experiment if applicable.
    :type score_min: float or str
    :param score_max: current max score for the experiment if applicable.
    :type score_max: float or str
    :param remote: flag whether this is a remote run or local run.
    :type remote: bool
    :param logger: logger for info/error messages.
    :param fit_iteration_parameters_dict: Remaining data specific parameters for fit such as 'x_raw_column_names'.
    :type fit_iteration: dict
    :param project: Deprecated parameter - replaced by experiment.
    :return: AzureML Run Properties for this child run
    :rtype: dict
    """
    if logger is None:
        logger = get_logger()

    _log_system_info(logger, prefix_message="[RunId:{}]".format(run_id))

    telemetry_logger = SystemResourceUsageTelemetryFactory.get_system_usage_telemetry(
        logger, interval=10)

    automl_settings = _AutoMLSettings.from_string_or_dict(
        automl_settings, experiment=experiment)

    _set_telemetry_collection(logger=logger, automl_settings=automl_settings)

    telemetry_logger.send_usage_telemetry_log(
        prefix_message="[RunId:{}][Starting fit_pipeline]".format(run_id),
        is_sending_telemetry=automl_settings.send_telemetry
    )

    # validate X and y
    _validate_training_data(X, y, X_valid, y_valid, sample_weight,
                            sample_weight_valid, cv_splits_indices, automl_settings)

    if remote:
        child_run_metrics = Run.get_context()
    else:
        child_run_metrics = Run(experiment,
                                run_id)

    logger.info("Created child run {0}".format(child_run_metrics.id))
    fit_output = {}
    fit_output_str = {}
    model_output = None
    errors = {}
    training_type = None
    runner = None
    dataset = None
    pipeline_spec = None
    try:
        metrics = None
        preprocess = automl_settings.preprocess
        class_labels = None

        enforce_time_on_windows = automl_settings.enforce_time_on_windows

        x_is_sparse = scipy.sparse.issparse(X)
        if x_is_sparse:
            # ignore preprocess if x is sparse
            preprocess = False

        telemetry_logger.send_usage_telemetry_log(
            prefix_message="[RunId:{}][Before preprocess]".format(run_id),
            is_sending_telemetry=automl_settings.send_telemetry
        )

        transformer, lag_transformer = None, None
        if preprocess is True or preprocess == "True":
            # Read raw feature names if they are available
            if fit_iteration_parameters_dict is not None and 'x_raw_column_names' in fit_iteration_parameters_dict:
                x_raw_column_names = fit_iteration_parameters_dict['x_raw_column_names']
            else:
                x_raw_column_names = None

            transformer, lag_transformer, X, X_valid = \
                _transform_data(logger, X, y, X_valid,
                                automl_settings.task_type, x_raw_column_names,
                                automl_settings.lag_length)

        telemetry_logger.send_usage_telemetry_log(
            prefix_message="[RunId:{}][After preprocess]".format(run_id),
            is_sending_telemetry=automl_settings.send_telemetry
        )

        # Data after transformation can be sparse
        x_is_sparse = scipy.sparse.issparse(X)
        enforce_time_on_win_required = False
        if automl_settings.max_time_sec is not None and \
                not safe_enforce_limits.ok and \
                enforce_time_on_windows and \
                os.name == 'nt':
            enforce_time_on_win_required = True

        # todo can move to helper, but not necessary
        _runtime_constraints = default_resource_limits.copy()
        _runtime_constraints['mem_in_mb'] = automl_settings.mem_in_mb
        _runtime_constraints['wall_time_in_s'] = automl_settings.max_time_sec

        goal = _get_iteration_goal(automl_settings)

        if automl_settings.task_type == "classification":
            class_labels = np.unique(y)

        telemetry_logger.send_usage_telemetry_log(
            prefix_message="[RunId:{}][Before executing pipeline]".format(
                run_id),
            is_sending_telemetry=automl_settings.send_telemetry
        )

        logger.info("Start executing pipeline {0}.".format(pipeline_script))

        try:
            if pipeline_id == constants.ENSEMBLE_PIPELINE_ID:
                is_ensemble_iteration = True
            else:
                is_ensemble_iteration = False

            if enforce_time_on_win_required:
                runner, dataset, pipeline_spec, training_type = \
                    _get_training_args(metrics,
                                       X,
                                       y,
                                       sample_weight,
                                       X_valid,
                                       y_valid,
                                       sample_weight_valid,
                                       automl_settings.validation_size,
                                       cv_splits_indices,
                                       automl_settings.n_cross_validations,
                                       automl_settings.num_classes,
                                       automl_settings.task_type,
                                       automl_settings.y_min,
                                       automl_settings.y_max,
                                       pipeline_script,
                                       automl_settings.max_cores_per_iteration)
                results, status = _train_pipeline_enforce_time_limit_on_windows(
                    metrics=metrics,
                    X=X,
                    y=y,
                    sample_weight=sample_weight,
                    X_valid=X_valid,
                    y_valid=y_valid,
                    sample_weight_valid=sample_weight_valid,
                    frac_valid=automl_settings.validation_size,
                    cv_splits_indices=cv_splits_indices,
                    num_cv_folds=automl_settings.n_cross_validations,
                    num_classes=automl_settings.num_classes,
                    task_type=automl_settings.task_type,
                    y_min=automl_settings.y_min,
                    y_max=automl_settings.y_max,
                    pipeline_spec=pipeline_spec,
                    max_time_sec=automl_settings.max_time_sec,
                    is_ensemble_iteration=is_ensemble_iteration)
            else:
                runner, dataset, pipeline_spec, training_type = \
                    _get_training_args(metrics,
                                       X,
                                       y,
                                       sample_weight,
                                       X_valid,
                                       y_valid,
                                       sample_weight_valid,
                                       automl_settings.validation_size,
                                       cv_splits_indices,
                                       automl_settings.n_cross_validations,
                                       automl_settings.num_classes,
                                       automl_settings.task_type,
                                       automl_settings.y_min,
                                       automl_settings.y_max,
                                       pipeline_script,
                                       automl_settings.max_cores_per_iteration,
                                       _runtime_constraints)
                results, status = runner.run_type(dataset,
                                                  pipeline_spec,
                                                  training_type=training_type,
                                                  is_ensemble_iteration=is_ensemble_iteration)

            if isinstance(status, BaseException):
                raise RuntimeError from status

            # for cross validation train the model on full data set.
            if results is not None and len(results) > 2:
                if training_type in \
                        [constants.TrainingType.CrossValidation, constants.TrainingType.MeanCrossValidation]:
                    result_full, status = runner.run_type(dataset, pipeline_spec,
                                                          training_type=constants.TrainingType.TrainFull)
                    if isinstance(status, BaseException):
                        raise RuntimeError from status

                    if result_full is None or len(result_full) <= 3:
                        raise ValueError("Failed while training full result.")

                    results = results[0], results[1], results[2], result_full[3]
        except Exception as e:
            errors['fit'] = {'exception': e,
                             'traceback': traceback.format_exc()}
            _log_traceback(e, logger)
            results = None

        telemetry_logger.send_usage_telemetry_log(
            prefix_message="[RunId:{}][After executing pipeline]".format(
                run_id),
            is_sending_telemetry=automl_settings.send_telemetry
        )

        if results is not None:
            score_valid, fit_time, _, fitted_pipeline = results
        else:
            fit_time = 0
            score_valid = constants.Defaults.INVALID_PIPELINE_VALIDATION_SCORES
            fitted_pipeline = constants.Defaults.INVALID_PIPELINE_FITTED

        score = constants.Defaults.DEFAULT_PIPELINE_SCORE
        if automl_settings.primary_metric in score_valid:
            score = score_valid[automl_settings.primary_metric]
        else:
            score_valid[automl_settings.primary_metric] = score
        logger.info(
            "Pipeline execution finished with a score of {0}".format(score))

        try:
            run_properties = str(pipeline_spec.steps[1][1])[str(pipeline_spec.steps[1][1]).find("(") + 1:
                                                            str(pipeline_spec.steps[1][1]).find(")")]
        except Exception:
            run_properties = None

        try:
            # for the Ensemble pipelines we will not have any preprocessors
            if len(pipeline_spec.steps) == 1:
                run_preprocessor = None
                run_algorithm = pipeline_spec.steps[0][0]
            else:
                run_preprocessor = pipeline_spec.steps[0][0]
                run_algorithm = pipeline_spec.steps[1][0]
        except Exception:
            run_preprocessor = None
            run_algorithm = None

        fit_output = {
            "staticProperties": {},
            "score": score,
            "run_preprocessor": run_preprocessor,
            "run_algorithm": run_algorithm,
            "run_properties": run_properties,
            "pipeline_script": pipeline_script,
            "pipeline_id": pipeline_id,
            "training_type": training_type,
            "num_classes": automl_settings.num_classes,
            "framework": "sklearn",
            "run_template": "automl_child",
            "experiment_id": experiment_id,
            "fit_time": fit_time,
            "goal": goal,
            "class_labels": class_labels,
            "primary_metric": automl_settings.primary_metric,
            "errors": errors,
        }

        dependencies = {'dependencies_versions': None}
        dependencies['dependencies_versions'] = json.dumps(
            get_sdk_dependencies())

        logger.info("Start logging metrics for child run.")

        _log_metrics(child_run_metrics, score_valid, logger)

        fit_output['fit_time'] = fit_time
        logger.info(
            "The following metrics have been logged for the child run: {0}.".format(score_valid))

        if isinstance(fitted_pipeline, list):
            fitted_pipeline = fitted_pipeline[0]

        if (transformer is not None or lag_transformer is not None) and \
                fitted_pipeline is not constants.Defaults.INVALID_PIPELINE_FITTED:
            fitted_pipeline = _add_transformer_x(
                transformer, lag_transformer, fitted_pipeline)

        fit_output['fitted_pipeline'] = fitted_pipeline

        # TODO: remove once backend can handle nulls
        fit_output_str = _sanitize_fit_output(fit_output)

        # todo can put in helper with code above, but maybe not necessary
        if automl_settings.metric_operation == constants.OptimizerObjectives.MINIMIZE:
            if score_min is None or score < float(score_min):
                score_min = score
            best_score = score_min
        elif automl_settings.metric_operation == constants.OptimizerObjectives.NA:
            best_score = float('nan')
        else:
            if score_max is None or score > float(score_max):
                score_max = score
            best_score = score_max

        child_run_metrics.log(goal, best_score)
        child_run_metrics.set_tags(fit_output_str)

        model_output = tempfile.NamedTemporaryFile(mode='wb+', delete=False)

        with(open(model_output.name, 'wb')):
            pickle.dump(fit_output['fitted_pipeline'], model_output)
            model_output.flush()
        with(open(model_output.name, 'rb')):
            child_run_metrics.upload_file(
                constants.MODEL_PATH, model_output.name)
        model_output.close()

        fit_output['pipeline_python_obj'] = pipeline_spec
        child_run_metrics.complete()
    except Exception as e:
        errors['overall'] = {'exception': e,
                             'traceback': traceback.format_exc()}
        _log_traceback(e, logger)
        child_run_metrics.fail()
    finally:
        fit_output['errors'] = errors
        if child_run_metrics is not None:
            # TODO: move to tags once JOS is updated
            child_run_metrics.add_properties(fit_output_str)
            child_run_metrics.add_properties(dependencies)
        if model_output is not None:
            model_output.close()
            os.unlink(model_output.name)
        # TODO: move to tags once rest of SDK has been converted
        fit_output['pipeline_spec'] = pipeline_script
        fit_output[automl_settings.primary_metric] = score_valid.get(automl_settings.primary_metric,
                                                                     constants.Defaults.DEFAULT_PIPELINE_SCORE)

        telemetry_logger.send_usage_telemetry_log(
            prefix_message="[RunId:{}][End fit_pipeline]".format(run_id),
            is_sending_telemetry=automl_settings.send_telemetry
        )
        return fit_output


def _get_training_type(training_type, folds=0):
    """
    Determine what type of training and validation to do based on user inputs

    :param training_type: str representing what type fo training and validation to do
    :param folds: int number of
    :return: None
    """
    valid_training_types = (constants.TrainingType.TrainAndValidation,
                            constants.TrainingType.MeanCrossValidation)
    if training_type not in valid_training_types:
        raise AssertionError(
            "%s and %s are the only supported training types." % valid_training_types)
    is_cv = training_type == constants.TrainingType.MeanCrossValidation
    if not ((is_cv and folds) or (not is_cv and not folds)):
        raise AssertionError("Cannot specify number of folds "
                             "if training type is not %s" % constants.TrainingType.MeanCrossValidation)
    if folds < 0 or folds == 1:
        raise AssertionError(
            "Cross validation folds must be greater than 1, got %d" % folds)
    return training_type


def _get_training_args(metrics,
                       X,
                       y,
                       sample_weight,
                       X_valid,
                       y_valid,
                       sample_weight_valid,
                       frac_valid,
                       cv_splits_indices,
                       num_cv_folds,
                       num_classes,
                       task_type,
                       y_min,
                       y_max,
                       pipeline_script=None,
                       max_cores_per_iteration=None,
                       runtime_constraints=None):

    dataset, training_type = _get_dataset(X=X,
                                          y=y,
                                          sample_weight=sample_weight,
                                          X_valid=X_valid,
                                          y_valid=y_valid,
                                          sample_weight_valid=sample_weight_valid,
                                          frac_valid=frac_valid,
                                          cv_splits_indices=cv_splits_indices,
                                          num_cv_folds=num_cv_folds,
                                          num_classes=num_classes,
                                          task_type=task_type,
                                          y_min=y_min,
                                          y_max=y_max,
                                          init_all_stats=False)
    problem_info = dataset.get_problem_info()
    problem_info.num_threads = max_cores_per_iteration
    is_sparse = scipy.sparse.issparse(X)
    pipeline_spec = None
    if pipeline_script:
        _, pipeline_spec = _get_pipeline(
            pipeline_script, problem_info, is_sparse)
    runner = ClientRunner(dataset, metrics=metrics,
                          task_type=task_type, runtime_constraints=runtime_constraints)
    return runner, dataset, pipeline_spec, training_type


def _train_pipeline_on_win_spawn_process(metrics,
                                         X,
                                         y,
                                         sample_weight,
                                         X_valid,
                                         y_valid,
                                         sample_weight_valid,
                                         frac_valid,
                                         cv_splits_indices,
                                         num_cv_folds,
                                         num_classes,
                                         task_type,
                                         y_min,
                                         y_max,
                                         pipeline_spec,
                                         is_ensemble_iteration: False):
    """
    :param metrics:
    :param X:
    :param y:
    :param X_valid:
    :param y_valid:
    :param frac_valid:
    :param cv_splits_indices:
    :param num_cv_folds:
    :param num_classes:
    :param task_type:
    :param y_min:
    :param y_max:
    :param pipeline_spec:
    :return:
    """

    from . import constants  # noqa: F401,F811
    from automl.client.core.common.datasets import ClientDatasets  # noqa: F401,F811
    from automl.client.core.common.model_wrappers import (
        LightGBMClassifier, SparseNormalizer, TruncatedSVDWrapper,
        CalibratedModel, FastICA, LightGBMRegressor, LinearSVMWrapper,
        NBWrapper, NuSVCWrapper, SGDClassifierWrapper, SVCWrapper)  # noqa: F401,F811
    from automl.client.core.common.exceptions import DataException, ServiceException  # noqa: F401,F811
    from automl.client.core.common.metrics import minimize_or_maximize  # noqa: F401,F811
    from automl.client.core.common.preprocess import DataTransformer, LaggingTransformer  # noqa: F401,F811
    from automl.client.core.common.runner_legacy import ClientRunner   # noqa: F401,F811
    import logging  # noqa: F401,F811
    import numpy as np  # noqa: F401,F811
    import pandas as pd  # noqa: F401,F811
    import pickle  # noqa: F401,F811
    import os  # noqa: F401,F811
    import os.path  # noqa: F401,F811
    import scipy  # noqa: F401,F811
    import sys  # noqa: F401,F811
    import tempfile  # noqa: F401,F811
    import traceback  # noqa: F401,F811
    import sklearn  # noqa: F401,F811
    from sklearn import pipeline, preprocessing, linear_model, decomposition, ensemble  # noqa: F401,F811
    from sklearn.metrics import recall_score, precision_score  # noqa: F401,F811
    from sklearn.model_selection import cross_val_score  # noqa: F401,F811
    from sklearn.pipeline import make_pipeline  # noqa: F401,F811
    from azureml.core.run import Run  # noqa: F401,F811
    try:
        runner, dataset, _, training_type = \
            _get_training_args(metrics,
                               X,
                               y,
                               sample_weight,
                               X_valid,
                               y_valid,
                               sample_weight_valid,
                               frac_valid,
                               cv_splits_indices,
                               num_cv_folds,
                               num_classes,
                               task_type,
                               y_min,
                               y_max)
        return runner.run_type(dataset,
                               pipeline_spec,
                               training_type=training_type,
                               is_ensemble_iteration=is_ensemble_iteration)
    except Exception as e:
        return None, e


def _train_pipeline_enforce_time_limit_on_windows(metrics,
                                                  X,
                                                  y,
                                                  sample_weight,
                                                  X_valid,
                                                  y_valid,
                                                  sample_weight_valid,
                                                  frac_valid,
                                                  cv_splits_indices,
                                                  num_cv_folds,
                                                  num_classes,
                                                  task_type,
                                                  y_min,
                                                  y_max,
                                                  pipeline_spec,
                                                  max_time_sec,
                                                  is_ensemble_iteration):
    '''

    :param metrics:
    :param X:
    :param y:
    :param X_valid:
    :param y_valid:
    :param frac_valid:
    :param cv_splits_indices:
    :param num_cv_folds:
    :param num_classes:
    :param task_type:
    :param y_min:
    :param y_max:
    :param pipeline_script:
    :param training_type:
    :param max_time_sec:
    :param sample_weight:
    :return:
    '''
    dict = {"metrics": metrics, "X": X, "y": y, "sample_weight": sample_weight,
            "X_valid": X_valid, "y_valid": y_valid, "sample_weight_valid": sample_weight_valid,
            "frac_valid": frac_valid, "cv_splits_indices": cv_splits_indices, "num_cv_folds": num_cv_folds,
            "num_classes": num_classes, "task_type": task_type, "y_min": y_min, "y_max": y_max,
            "pipeline_spec": pipeline_spec, "is_ensemble_iteration": is_ensemble_iteration}
    return enforce_time_limit(max_time_sec, _train_pipeline_on_win_spawn_process, dict)


def _get_dataset(X,
                 y,
                 sample_weight=None,
                 frac_valid=0.0,
                 X_valid=None,
                 y_valid=None,
                 sample_weight_valid=None,
                 cv_splits_indices=None,
                 num_cv_folds=0,
                 num_classes=None,
                 task_type="classification",
                 y_min=None,
                 y_max=None,
                 init_all_stats=False):
    """

    :param X:
    :param y:
    :param frac_valid:
    :param X_valid:
    :param y_valid:
    :param num_cv_folds:
    :param num_classes:
    :return:
    """
    assert_failures = []

    dataset = ClientDatasets()
    if X_valid is not None:
        training_type = _get_training_type(
            constants.TrainingType.TrainAndValidation)

        if not (num_cv_folds == 0 or num_cv_folds is None):
            assert_failures.append(
                'n_cross_validations cannot be specified when X_valid is provided.')

        if not (frac_valid == 0.0 or frac_valid is None):
            assert_failures.append(
                'validation_size cannot be specified when X_valid is provided.')

        if y_valid is None:
            assert_failures.append(
                'y_valid must also be provided when X_valid is provided.')

        if len(assert_failures) > 0:
            raise AssertionError("Bad fit parameters. Please review documentation for fit. " +
                                 ' '.join(assert_failures))
        dataset.parse_simple_train_validate(name="NoName",
                                            X=X,
                                            y=y,
                                            sample_weight=sample_weight,
                                            X_valid=X_valid,
                                            y_valid=y_valid,
                                            sample_weight_valid=sample_weight_valid,
                                            task=task_type,
                                            y_min=y_min,
                                            y_max=y_max,
                                            init_all_stats=init_all_stats)

    else:
        if y_valid is not None:
            assert_failures.append(
                'y_valid should only be provided when X_valid is provided.')
        if(num_cv_folds == 0 or num_cv_folds is None) and cv_splits_indices is None:
            training_type = _get_training_type(
                constants.TrainingType.TrainAndValidation)
            if frac_valid <= 0.0:
                assert_failures.append('frac_valid must be greater than zero.')
        else:
            if cv_splits_indices is not None:
                num_cv_folds = len(cv_splits_indices)
            training_type = _get_training_type(
                constants.TrainingType.MeanCrossValidation, num_cv_folds)

        if len(assert_failures) > 0:
            raise AssertionError("Bad fit parameters. Please review documentation for fit. " +
                                 ' '.join(assert_failures))

        dataset.parse_data(name="NoName",
                           X=X,
                           y=y,
                           sample_weight=sample_weight,
                           perc_valid=frac_valid,
                           perc_test=0.0,
                           cv_splits_indices=cv_splits_indices,
                           CV=num_cv_folds,
                           num_classes=num_classes,
                           task=task_type,
                           y_min=y_min,
                           y_max=y_max,
                           init_all_stats=init_all_stats)
    return dataset, training_type


def _get_pipeline(pipeline_script, problem_info, is_sparse):
    """

    :param pipeline_script: returned from service that is a dictionary of pipeline
    : spec
    : or for backward compatibility a dictionary of normal and sparse pipeline
    : definition that can be eval'd
    :param problem_info: The metadata on the dataset.
    :param is_sparse: True/False depending on whether the inputs are sparse
    :return:
    """

    try:
        pipeline_dict = json.loads(pipeline_script)
    except ValueError:
        pipeline_dict = None
    if not pipeline_dict or "objects" not in pipeline_dict:
        return _get_pipeline_legacy(pipeline_script, is_sparse)

    return _get_pipeline_from_dict(pipeline_dict, problem_info, is_sparse)


def _get_pipeline_from_dict(pipeline_dict, problem_info, is_sparse):
    """

    :param pipeline_script: returned from service that is a dictionary of pipeline
    :spec
    :param problem_info: The metadata on the dataset.
    :param is_sparse: True/False depending on whether the inputs are sparse
    :return:
    """

    # replace standard scaler with wrapper.
    scaler = [o for o in pipeline_dict["objects"]
              if o['spec_class'] == pipeline_spec.PREPROC_NAME and o['class_name'] == 'StandardScaler']
    if len(scaler) == 1:
        scaler[0]['class_name'] = 'StandardScalerWrapper'
        scaler[0]['module'] = SOURCE_WRAPPER_MODULE

    spec = pipeline_spec.PipelineSpec.from_dict(pipeline_dict)
    pipeline = spec.instantiate_pipeline_spec(
        problem_info, is_sparse=is_sparse)
    return pipeline_dict, pipeline


def _get_pipeline_legacy(pipeline_script, is_sparse):
    """

    :param pipeline_script: returned from service that can be either a json or a string to be eval'd
    :param is_sparse: True/False depending on whether the inputs are sparse
    :return:
    """
    pipeline_spec = eval(pipeline_script)
    sparse_strs = {True: "sparse", False: "normal"}

    if not isinstance(pipeline_spec, dict):
        return pipeline_script, pipeline_spec
    else:
        script = pipeline_spec[sparse_strs[is_sparse]]
        return script, eval(script)


def _add_transformer_x(transformer, lag_transformer, pipeline_spec):
    """
    Adds transformer as first step of the pipeline

    :param pipeline_spec: pipeline to which the transformer should be added
    :param transformer: a pipeline compatible transformation that implements fit, transform and predict
    :return: pipeline with transformer prepended
    """
    transformers = filter(lambda x: x is not None, [
                          transformer, lag_transformer])

    return make_pipeline(*transformers, *[s[1] for s in pipeline_spec.steps])


def _get_transformer_x(x, y, task_type, logger=None):
    """
    Given data, compute transformations and transformed data

    :param x: input data
    :param y: labels
    :param task_type: one of the tasks defined in constants.Tasks
    :return: transformer, transformed_x
    """

    dt = DataTransformer(task_type)
    x_transform = dt.fit_transform_with_logger(x, y, logger)

    return dt, x_transform


def _evaluate_pipeline(pipeline_string):
    """

    :param pipeline_string:
    :return:
    """
    return eval(pipeline_string)


def _add_raw_column_names_to_X(x_raw_column_names, X):
    """
    Add raw column names to X

    :param x_raw_column_names: List of raw column names
    :param X: dataframe / array
    :raise ValueError if number of raw column names is not same as the number of columns in X
    :return: Dataframe with column names
    """
    # Combine the raw feature names with X
    if x_raw_column_names is not None:
        if x_raw_column_names.shape[0] != X.shape[1]:
            raise DataException("Number of raw column names " + x_raw_column_names.shape[0] +
                                "and number of columns in input data " + X.shape[1] + " do not match")

        X_with_raw_columns = pd.DataFrame(
            data=X, columns=x_raw_column_names.tolist())

        return X_with_raw_columns

    return X


def _sanitize_fit_output(fit_output):
    # TODO: remove once backend can handle nulls
    fit_output_str = {}
    for key in fit_output:
        if fit_output[key] is None:
            fit_output_str[key] = ''
        else:
            fit_output_str[key] = str(fit_output[key])
    return fit_output_str


def _log_metrics(child_run, score_valid, logger):
    for m in score_valid:
        try:
            if isinstance(score_valid[m], float):
                child_run.log(m, float(score_valid[m]))
            elif isinstance(score_valid[m], np.ndarray):
                child_run.log_list(m, score_valid[m].flatten())
            elif isinstance(score_valid[m], dict):
                if m == 'confusion_matrices':
                    for key in score_valid[m].keys():
                        score_valid[m][key] = (
                            score_valid[m][key].flatten()).tolist()
                uniform_arr_len = np.max(
                    [len(score_valid[m][x]) for x in score_valid[m]])
                for key in score_valid[m]:
                    while len(score_valid[m][key]) != uniform_arr_len:
                        score_valid[m][key] = np.append(
                            score_valid[m][key], np.nan)
                child_run.log_table(m, score_valid[m])
        except Exception as e:
            logger.warning(
                "Failed to log the metric {metric} with value {metric_value}".format(metric=m,
                                                                                     metric_value=str(score_valid[m])))
            _log_traceback(e, logger)


def _set_telemetry_collection(logger, automl_settings):
    """
    Sets telemetry collection based on automl settings

    :param logger: logger object
    :param automl_settings: automl settings
    :return: None
    """
    if not automl_settings.send_telemetry:
        return

    try:
        level = logging._checkLevel(automl_settings.telemetry_verbosity)

        if level is not logging.NOTSET:
            set_diagnostics_collection(send_diagnostics=True, verbosity=level)
            found_telemetry_handler = False

            for handler in logger.handlers:
                if isinstance(handler, AppInsightsLoggingHandler):
                    found_telemetry_handler = True
                    break

            if not found_telemetry_handler:
                logger.addHandler(get_telemetry_log_handler())
    except Exception:
        pass  # do nothing


def _get_iteration_goal(automl_settings):
    goal = None
    if automl_settings.metric_operation == constants.OptimizerObjectives.MINIMIZE:
        goal = automl_settings.primary_metric + "_min"
    elif automl_settings.metric_operation == constants.OptimizerObjectives.MAXIMIZE:
        goal = automl_settings.primary_metric + "_max"
    elif automl_settings.metric_operation == constants.OptimizerObjectives.NA:
        goal = automl_settings.primary_metric + "_NA"
    else:
        raise NotImplementedError()

    return goal
