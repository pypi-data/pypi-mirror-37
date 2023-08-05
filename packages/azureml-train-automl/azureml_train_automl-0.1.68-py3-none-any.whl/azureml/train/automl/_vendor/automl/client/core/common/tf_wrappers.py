# Copyright (c) 2018 Microsoft Corporation.  All rights reserved.
"""Wraper classes for running TF pipelines."""
import copy
import gc
import math
import os
import time

import numpy as np
import pandas as pd
import scipy
import sklearn
from sklearn.base import BaseEstimator
import tensorflow as tf
from tensorflow.python.estimator.canned import prediction_keys

from automl.client.core.common import constants

HASH_BUCKET_SIZE = 1000
WEIGHTS_COLUMN = 'sample_weight'
IS_SPARSE = 'is_sparse'
COLUMN = 'column'

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.logging.set_verbosity(tf.logging.ERROR)

OPTIMIZERS = {
    'sgd': tf.train.GradientDescentOptimizer,
    'adagrad': tf.train.AdagradOptimizer,
    'momentum': tf.train.MomentumOptimizer,
    'adam': tf.train.AdamOptimizer,
    'ftrl': tf.train.FtrlOptimizer,
    'rmsprop': tf.train.RMSPropOptimizer
}

ACTIVATION_FNS = {
    'relu': tf.nn.relu,
    'crelu': tf.nn.crelu,
    'elu': tf.nn.elu,
    'selu': tf.nn.selu,
    'sigmoid': tf.sigmoid,
    'softplus': tf.nn.softplus,
    'softsign': tf.nn.softsign,
    'tanh': tf.tanh
}


class RuntimeRunHook(tf.train.SessionRunHook):

    # TODO: this safety margin value is a dumb way to allow enough time
    # for the pipeline to predict.  The real solution is to not include
    # prediction in the time constrainer, but doing that relies on
    # doing something else other than killing a multiprocess, because
    # we have to get a model object back from it.
    def __init__(self, max_time, safety_margin=5):
        self._max_time = max_time
        self._safety_margin = safety_margin
        self._start = time.time()

    def after_run(self, run_context, run_values):
        if time.time() - self._start >= self._max_time - self._safety_margin:
            tf.logging.info('Stopping...')
            run_context.request_stop()


class _EstimatorWrapper(BaseEstimator):
    def __init__(self, est_class, task, arg_params, batch_size=1024, **params):
        self._est_cls = est_class
        self._task = task
        self._est = None
        self._arg_params = arg_params
        self._params = params
        self._batch_size = batch_size
        self._num_epochs = None
        self._max_time = None
        self._is_nan_error = False
        self._feature_columns = None
        self._is_sparse = False

    @staticmethod
    def get_sparse_feature_columns(X):
        csr = X.tocsr()
        col = []
        for i in range(csr.shape[1]):
            col_vect = csr[i]
            c_name = str(i)
            # all sparse columns are treated as categorical
            # and embedded to produce the dense feature required
            # by DNNs.
            if csr.shape[0] == col_vect.nnz:
                col.append(_EstimatorWrapper._create_feature_column(
                    tf.feature_column.numeric_column(c_name)))
            else:
                c = tf.feature_column.categorical_column_with_hash_bucket(
                    c_name,
                    HASH_BUCKET_SIZE,
                    dtype=tf.int32)
                ec = tf.feature_column.embedding_column(c, 1)
                col.append(_EstimatorWrapper._create_feature_column(ec, True))
        return col

    @staticmethod
    def _create_feature_column(column, is_sparse=False):
        return {COLUMN: column, IS_SPARSE: is_sparse}

    def get_feature_columns(self, X):
        if self._feature_columns is None:
            if isinstance(X, np.ndarray):
                self._feature_columns = \
                    [_EstimatorWrapper._create_feature_column(
                        tf.feature_column.numeric_column(str(i)))
                        for i in range(X.shape[1])]
            elif scipy.sparse.issparse(X):
                self._is_sparse = True
                self._feature_columns = \
                    _EstimatorWrapper.get_sparse_feature_columns(X)
            elif isinstance(X, pd.DataFrame):
                column_types = X.dtypes
                numerical_features = \
                    [_EstimatorWrapper._create_feature_column(
                        tf.feature_column.numeric_column(cn))
                     for cn in column_types.index
                     if str(column_types[cn])[0:3] in ['int', 'flo']]
                catergorical_features = \
                    [_EstimatorWrapper._create_feature_column(
                        tf.feature_column.
                        categorical_column_with_hash_bucket(cn,
                                                            HASH_BUCKET_SIZE))
                     for cn in column_types.index
                     if str(column_types[cn])[0:3] not in ['int', 'flo']]
                self._feature_columns =\
                    numerical_features + catergorical_features
            else:
                raise NotImplementedError("Supported only numpy ndarray "
                                          "and sparse matrix")

        return [fc[COLUMN] for fc in self._feature_columns]

    def get_inp_features_sparse(self, X, sample_weight=None, y=None,
                                batch_size=10, shuffle=False, **kwargs):
        csr = X.tocsr()
        features = {}
        for i in range(csr.shape[1]):
            col_vect = csr[:, i]
            if self._feature_columns[i][IS_SPARSE]:
                coo = col_vect.tocoo()
                # casting the sparse vectors into category.
                int_data = [int(d) for d in coo.data]
                vect = tf.SparseTensor(indices=[[i, 0] for i in coo.row],
                                       values=int_data,
                                       dense_shape=[X.shape[0], 1])
            else:
                vect = col_vect.todense().reshape(-1, 1)
            features[str(i)] = vect
        if sample_weight is not None:
            features[WEIGHTS_COLUMN] = sample_weight
        if y is None:
            dataset = tf.data.Dataset.from_tensor_slices(dict(features))
        else:
            dataset = tf.data.Dataset.from_tensor_slices((dict(features), y))
        if shuffle:
            dataset = dataset.shuffle(batch_size)
        return dataset.batch(batch_size)

    def _get_sparse_input_fn(self, X, sample_weight, **kwargs):
        return lambda: self.get_inp_features_sparse(X, **kwargs)

    def _get_input_fn(self, X, sample_weight=None, **kwargs):
        if isinstance(X, np.ndarray):
            column_dict = {str(i): X[:, i] for i in range(X.shape[1])}
            # sparse columns are treated as categorical and should be int.
            if self._is_sparse:
                for col, feat in enumerate(self._feature_columns):
                    if feat[IS_SPARSE]:
                        if str(col) in column_dict:
                            column_dict[str(col)] = \
                                column_dict[str(col)].astype(int)

            if sample_weight is not None:
                column_dict[WEIGHTS_COLUMN] = sample_weight
            return tf.estimator.inputs.numpy_input_fn(
                column_dict, **kwargs)

        elif isinstance(X, pd.DataFrame):
            if sample_weight is not None:
                X[WEIGHTS_COLUMN] = sample_weight
            return tf.estimator.inputs.pandas_input_fn(
                X, **kwargs)
        elif scipy.sparse.issparse(X):
            assert self._is_sparse
            return self._get_sparse_input_fn(X, sample_weight, **kwargs)
        else:
            raise NotImplementedError(
                'input with type {0} not supported.'.format(type(X)))

    def _construct_estimator(self, X, sample_weight=None):
        kwargs = copy.deepcopy(self._params)
        kwargs['feature_columns'] = self.get_feature_columns(X)

        if sample_weight is not None:
            kwargs['weight_column'] = tf.feature_column.numeric_column(
                WEIGHTS_COLUMN)

        if ('hidden_layer_width_frac' in kwargs and
                'num_hidden_layers' in kwargs):
            width = math.ceil(kwargs.pop(
                'hidden_layer_width_frac') * X.shape[1])
            kwargs['hidden_units'] = [width] * \
                int(kwargs.pop('num_hidden_layers'))

        if 'max_time' in kwargs:
            self._max_time = kwargs.pop('max_time')

        self._num_epochs = int(kwargs.pop('num_epochs'))
        if 'seed' in kwargs:
            tf.set_random_seed(kwargs.pop('seed'))
        args = tuple([kwargs.pop(a) for a in self._arg_params])
        self._est = self._est_cls(*args, **kwargs)

    def fit(self, X, y, sample_weight=None):
        self._construct_estimator(X, sample_weight=sample_weight)

        # TODO: consider a max-steps approach that is calculated from
        # self._num_epochs, instead of passing num_epochs to the input_fn.
        kwargs = {'batch_size': self._batch_size,
                  'shuffle': True,
                  'y': y,
                  'num_epochs': self._num_epochs}

        hooks = []
        if self._max_time is not None:
            hooks.append(RuntimeRunHook(self._max_time))
        try:
            self._est.train(self._get_input_fn(
                X, sample_weight=sample_weight, **kwargs),
                hooks=hooks)
        except tf.train.NanLossDuringTrainingError:
            self._is_nan_error = True
        # Explicitly call garbage collector, see github issue:
        # https://github.com/tensorflow/tensorflow/issues/14181
        gc.collect()
        return self

    def partial_fit(self, X, y, sample_weight=None):
        if not self._est:
            self._construct_estimator(X, sample_weight=sample_weight)
        kwargs = {'batch_size': self._batch_size,
                  'shuffle': True,
                  'y': y,
                  'num_epochs': self._num_epochs}

        self._est.train(self._get_input_fn(
            X, sample_weight=sample_weight, **kwargs))
        gc.collect()
        return self

    def predict(self, X):
        kwargs = {'batch_size': self._batch_size,
                  'shuffle': False}
        if self._task == constants.Tasks.CLASSIFICATION:
            predict_keys = prediction_keys.PredictionKeys.CLASS_IDS
        elif self._task == constants.Tasks.REGRESSION:
            predict_keys = prediction_keys.PredictionKeys.PREDICTIONS
        else:
            raise NotImplementedError()
        predictions = self._est.predict(
            self._get_input_fn(X, **kwargs),
            predict_keys=predict_keys)
        gc.collect()
        ret = np.array([p[predict_keys] for p in predictions])
        assert X.shape[0] == ret.shape[0]
        return ret

    def predict_proba(self, X):
        if self._task == constants.Tasks.REGRESSION:
            raise ValueError('Running predict_proba for regression.')

        kwargs = {'batch_size': self._batch_size,
                  'shuffle': False}

        predictions = self._est.predict(
            self._get_input_fn(X, **kwargs),
            predict_keys=prediction_keys.PredictionKeys.PROBABILITIES)
        gc.collect()
        ret = np.array([p[prediction_keys.PredictionKeys.PROBABILITIES]
                        for p in predictions])
        assert X.shape[0] == ret.shape[0]
        return ret


class TFLinearClassifierWrapper(_EstimatorWrapper):

    def __init__(self, **kwargs):
        super(TFLinearClassifierWrapper, self).__init__(
            tf.estimator.LinearClassifier, constants.Tasks.CLASSIFICATION,
            ['feature_columns'], **kwargs)


class TFDNNClassifierWrapper(_EstimatorWrapper):

    def __init__(self, **kwargs):
        super(TFDNNClassifierWrapper, self).__init__(
            tf.estimator.DNNClassifier, constants.Tasks.CLASSIFICATION,
            ['hidden_units', 'feature_columns'], **kwargs)


class TFLinearRegressorWrapper(_EstimatorWrapper):

    def __init__(self, **kwargs):
        super(TFLinearRegressorWrapper, self).__init__(
            tf.estimator.LinearRegressor, constants.Tasks.REGRESSION,
            ['feature_columns'], **kwargs)


class TFDNNRegressorWrapper(_EstimatorWrapper):

    def __init__(self, **kwargs):
        super(TFDNNRegressorWrapper, self).__init__(
            tf.estimator.DNNRegressor, constants.Tasks.REGRESSION,
            ['hidden_units', 'feature_columns'], **kwargs)
