# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""AutoML SDK utilities."""

import numpy as np
import pandas as pd
import scipy

from automl.client.core.common.utilities import (
    _check_if_column_data_type_is_numerical,
    _get_column_data_type_as_str,
    _check_dimensions
)

from automl.client.core.common.exceptions import ServiceException

from . import _constants_azureml
from . import constants
from .constants import Metric


def _check_sample_weight(x, sample_weight, x_name,
                         sample_weight_name, automl_settings):
    """
    Validate sample_weight.

    :param x:
    :param sample_weight:
    :raise ValueError if sample_weight has problems
    :return:
    """
    if not isinstance(sample_weight, np.ndarray):
        raise ValueError(sample_weight_name + " should be numpy array")

    if x.shape[0] != len(sample_weight):
        raise ValueError(sample_weight_name +
                         " length should match length of " + x_name)

    if len(sample_weight.shape) > 1:
        raise ValueError(sample_weight_name +
                         " should be a unidimensional vector")

    if automl_settings.primary_metric in \
            Metric.SAMPLE_WEIGHTS_UNSUPPORTED_SET:
        raise ValueError("Sample weights is not supported for these"
                         " primary metrics: {0}".format(
                             Metric.SAMPLE_WEIGHTS_UNSUPPORTED_SET))


def _check_x_y(x, y, automl_settings):
    """
    Validate input data.

    :param x: input data. dataframe/ array/ sparse matrix
    :param y: input labels. dataframe/series/array
    :param automl_settings: automl settings
    :raise: ValueError if data does not conform to accepted types and shapes
    :return:
    """
    preprocess = automl_settings.preprocess

    # If text data is not being preprocessed or featurized, then raise an error
    if not (preprocess is True or preprocess == "True"):
        if isinstance(x, pd.DataFrame):
            for column in x.columns:
                if not _check_if_column_data_type_is_numerical(_get_column_data_type_as_str(x[column].values)):
                    raise ValueError("The training data contains text. Please set preprocess flag as true")
        elif isinstance(x, np.ndarray):
            for array in x:
                if not _check_if_column_data_type_is_numerical(_get_column_data_type_as_str(array)):
                    raise ValueError("The training data contains text. Please set preprocess flag as true")

    if not (((preprocess is True or preprocess == "True") and
             isinstance(x, pd.DataFrame)) or
            isinstance(x, np.ndarray) or scipy.sparse.issparse(x)):
        raise ValueError(
            "x should be dataframe with preprocess set or numpy array"
            " or sparse matrix")

    if not isinstance(y, np.ndarray):
        raise ValueError("y should be numpy array")

    if x.shape[0] != y.shape[0]:
        raise ValueError("number of rows in x and y are not equal")

    if len(y.shape) > 2 or (len(y.shape) == 2 and y.shape[1] != 1):
        raise ValueError("y should be a vector Nx1")

    if automl_settings.task_type == constants.Tasks.CLASSIFICATION:
        if y.dtype.kind != 'i':
            raise ValueError("Please label encode y as an integer array for"
                             " classification")

    if automl_settings.task_type == constants.Tasks.REGRESSION:
        if not _check_if_column_data_type_is_numerical(
                _get_column_data_type_as_str(y)):
            raise ValueError(
                "Please make sure y is numerical before fitting for "
                "regression")


def _validate_training_data(
        X, y, X_valid, y_valid, sample_weight, sample_weight_valid,
        cv_splits_indices, automl_settings):
    _check_x_y(X, y, automl_settings)

    # validate sample weights if not None
    if sample_weight is not None:
        _check_sample_weight(X, sample_weight, "X",
                             "sample_weight", automl_settings)

    if X_valid is not None and y_valid is None:
        raise ValueError(
            "X validation provided but y validation data is missing.")

    if y_valid is not None and X_valid is None:
        raise ValueError(
            "y validation provided but X validation data is missing.")

    if X_valid is not None and sample_weight is not None and \
            sample_weight_valid is None:
        raise ValueError("sample_weight_valid should be set to a valid value")

    if sample_weight_valid is not None and X_valid is None:
        raise ValueError(
            "sample_weight_valid should only be set if X_valid is set")

    if sample_weight_valid is not None:
        _check_sample_weight(X_valid, sample_weight_valid,
                             "X_valid", "sample_weight_valid", automl_settings)

    _check_dimensions(
        X=X, y=y, X_valid=X_valid, y_valid=y_valid,
        sample_weight=sample_weight, sample_weight_valid=sample_weight_valid)

    if X_valid is not None:
        if automl_settings.n_cross_validations is not None and \
                automl_settings.n_cross_validations > 0:
            raise ValueError("Both custom validation data and "
                             "n_cross_validations specified. "
                             "If you are providing the training "
                             "data, do not pass any n_cross_validations.")
        if automl_settings.validation_size is not None and \
                automl_settings.validation_size > 0.0:
            raise ValueError("Both custom validation data and "
                             "validation_size specified. If you are "
                             "providing the training data, do not pass "
                             "any validation_size.")
        if automl_settings.task_type == constants.Tasks.CLASSIFICATION:
            # y_valid should be a subset of y(training sample)
            in_train = set(y)
            in_valid = set(y_valid)
            only_in_valid = in_valid - in_train
            if len(only_in_valid) > 0:
                raise ValueError(
                    "y values in validation set should be a subset of "
                    "y values of training set.")

    if cv_splits_indices is not None:
        if automl_settings.n_cross_validations is not None and \
                automl_settings.n_cross_validations > 0:
            raise ValueError("Both cv_splits_indices and n_cross_validations "
                             "specified. If you are providing the indices to "
                             "use to split your data. Do not pass any "
                             "n_cross_validations.")
        if automl_settings.validation_size is not None and \
                automl_settings.validation_size > 0.0:
            raise ValueError("Both cv_splits_indices and validation_size "
                             "specified. If you are providing the indices to "
                             "use to split your data. Do not pass any "
                             "validation_size.")
        if X_valid is not None:
            raise ValueError("Both cv_splits_indices and custom split "
                             "validation data specified. If you are providing "
                             "the training data, do not pass any indices to "
                             "split your data.")


def friendly_http_exception(exception, api_name):
    """
    This function returns a details exception for an http exception.

    :param exception: Exception.
    :param api_name: string.
    :raise: ServiceException
    """
    try:
        # Raise bug with msrest team that response.status_code is always 500
        status_code = exception.error.response.status_code
        if status_code == 500:
            message = exception.message
            substr = 'Received '
            status_code = message[message.find(
                substr) + len(substr): message.find(substr) + len(substr) + 3]
    except Exception:
        raise exception

    if status_code in _constants_azureml.HTTP_ERROR_MAP:
        http_error = _constants_azureml.HTTP_ERROR_MAP[status_code]
    else:
        http_error = _constants_azureml.HTTP_ERROR_MAP['default']
    if api_name in http_error:
        error_message = http_error[api_name]
    else:
        error_message = http_error['default']
    raise ServiceException("{0} error raised. {1}".format(
        http_error['Name'], error_message)) from exception


def _get_primary_metrics(task):
    """Gets the primary metrics supported for a given task as a list
    :param task: string "classification" or "regression"
    :return: a list of the primary metrics supported for the task
    """
    if task == constants.Tasks.CLASSIFICATION:
        return list(constants.Metric.CLASSIFICATION_PRIMARY_SET)
    elif task == constants.Tasks.REGRESSION:
        return list(constants.Metric.REGRESSION_PRIMARY_SET)
    else:
        raise NotImplemented("Task {task} is not supported currently."
                             .format(task=task))
