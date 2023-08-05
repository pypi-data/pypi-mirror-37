# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Class for processing datasets for training/validation."""
import copy

import numpy as np
import scipy
import sklearn
from sklearn import model_selection

from automl.client.core.common import constants, problem_info
from automl.client.core.common.utilities import sparse_isnan, sparse_std


class ClientDatasets(object):
    """
    The object to stote the experiment input data and training charateristics
    """

    def __init__(self, meta_data=None):
        """
        Various methods for processing datasets for training/validation.
        :param meta_data: metedata to be directly set on the dataset
        """
        self._dataset = meta_data or {}
        self.binary_fields = [
            'X', 'y', 'train indices',
            'test indices', 'valid indices', 'train CV splits']
        self.meta_fields = [
            'dataset_id', 'num_samples', 'num_features', 'num_categorical',
            'num_classes', 'num_missing', 'y_mean', 'y_std', 'y_min', 'y_max',
            'X_mean', 'X_std', 'task', 'openml_id', 'name', 'is_sparse',
            'class_labels']
        self._subsample_cache = {}

    def get_y_range(self):
        """
        Gets the range of y values.
        :return: The y_min and y_max value.
        """
        y_min, y_max = None, None
        if 'y_min' in self._dataset:
            y_min = self._dataset['y_min']
        if 'y_max' in self._dataset:
            y_max = self._dataset['y_max']
        return y_min, y_max

    def get_full_set(self):
        """
        returns the full dataset sample data and label
        :return: return the full dataset
        """
        X, y = self._dataset['X'], self._dataset['y']
        sample_weight = self._dataset.get('sample_weight')
        return X, y, sample_weight

    def get_train_set(self):
        """
        returns the training part of the dataset
        :return:
        """
        X, y = self._dataset['X'], self._dataset['y']
        sample_weight = self._dataset.get('sample_weight')
        X_train, y_train = X[self._dataset['train indices']
                             ], y[self._dataset['train indices']]
        sample_weight_train = None \
            if sample_weight is None \
            else sample_weight[self._dataset['train indices']]

        return X_train, y_train, sample_weight_train

    def get_valid_set(self):
        """
        returns the validation part of the dataset
        :return:
        """
        X, y = self._dataset['X'], self._dataset['y']
        sample_weight = self._dataset.get('sample_weight')

        if 'X_valid' in self._dataset:
            assert 'y_valid' in self._dataset
            X_valid, y_valid, sample_weight_valid = (
                self._dataset['X_valid'],
                self._dataset['y_valid'],
                None)
            if sample_weight is not None:
                sample_weight_valid = self._dataset['sample_weight_valid']
        else:
            X_valid, y_valid = (
                X[self._dataset['valid indices']],
                y[self._dataset['valid indices']])
            sample_weight_valid = (None
                                   if sample_weight is None
                                   else sample_weight[
                                       self._dataset['valid indices']])

        return X_valid, y_valid, sample_weight_valid

    def get_test_set(self):
        """
        Get the test set from the full dataset
        :return: Test features, test labels, and weights of test samples
        :rtype: tuple(np.ndarray, np.ndarray, np.ndarray)
        """
        X, y = self._dataset['X'], self._dataset['y']
        sample_weight = self._dataset.get('sample_weight')
        if 'X_test' in self._dataset:
            assert 'y_test' in self._dataset.keys()
            X_test, y_test = self._dataset['X_test'], self._dataset['y_test']
            sample_weight_test = self._dataset['sample_weight_test']
        else:
            X_test, y_test = X[self._dataset['test indices']
                               ], y[self._dataset['test indices']]
            sample_weight_test = (sample_weight and
                                  sample_weight[self._dataset['test indices']])

        return X_test, y_test, sample_weight_test

    def has_test_set(self):
        """
        returns if the given dataset has test set available
        :return:
        """
        return 'X_test' in self._dataset or 'test indices' in self._dataset

    def get_CV_splits(self):
        """
        gets the CV splits of the dataset, if cross validation is specified.
        :return:
        """
        sample_wt = self._dataset.get('sample_weight')
        for train_ind, test_ind in self._dataset['train CV splits']:
            yield (self._dataset['X'][train_ind],
                   self._dataset['y'][train_ind],
                   None if sample_wt is None else sample_wt[train_ind],
                   self._dataset['X'][test_ind],
                   self._dataset['y'][test_ind],
                   None if sample_wt is None else sample_wt[test_ind])

    def get_num_classes(self):
        """
        gets the number of classes in the dataset.
        :return:  number of classes
        """
        return self.get_meta('num_classes')

    def get_task(self):
        """
        return the current task type
        :return:  task type such as regression or classification.
        """
        return self.get_meta('task')

    def get_meta(self, attr):
        """
        returns the value of the dataset attribute such as task, y_max
        :param attr:  the attribute to get
        :return: returns the value of the passed attribute
        """
        return self._dataset.get(attr, None)

    def add_data(self, attr, val):
        """
        sets the value of a datasetattribute
        :param attr: the attribute to set the value
        :param val: the value of the attribute
        :return: none
        """
        self._dataset[attr] = val

    def get_problem_info(self):
        """
        returns the _ProblemInfo of the dataset
        :return:
        """
        return problem_info.ProblemInfo(
            dataset_samples=self.get_meta('num_samples'),
            dataset_classes=self.get_num_classes(),
            dataset_features=self.get_meta('num_features'),
            dataset_num_categorical=self.get_meta('num_categorical'),
            dataset_y_std=self.get_meta('y_std'),
            is_sparse=self.get_meta('is_sparse'),
            task=self.get_meta('task'),
            metric=None)

    def _init_dataset(self, name, task, X, y, sample_weight=None,
                      categorical=None, openml_id=None, num_classes=None,
                      y_min=None, y_max=None, init_all_stats=True):
        """
        Initialize the data set with the input data, metadata and labels
        :param name:
        :param X: train data
        :param y: label for train data
        :param task: the task type of training(regression/classification)
        :param sample_weight: size of the sample
        :param categorical: is it categorical?
        :param openml_id:
        :param num_classes: number of classes in the experiment.
        :param y_min: min value of the label
        :param y_max: max value of the label
        :param init_all_stats:
        :return:
        """
        self._dataset = {}
        if openml_id is not None:
            self._dataset['openml_id'] = openml_id
        else:
            self._dataset['openml_id'] = 'NA'
        self._dataset['dataset_id'] = name
        self._dataset['name'] = name
        self._dataset['num_samples'] = int(X.shape[0])
        self._dataset['num_features'] = int(X.shape[1])
        self._dataset['num_missing'] = 0 if scipy.sparse.issparse(
            X) else int(np.sum(np.isnan(X)))
        self._dataset['y_std'] = float(y.std())
        if init_all_stats:
            self._dataset['y_mean'] = float(y.mean())
            self._dataset['X_mean'] = float(X.mean())
            self._dataset['X_std'] = float(
                X.std()) if not scipy.sparse.issparse(X) else sparse_std(X)
            self._dataset['is_sparse'] = scipy.sparse.issparse(X)
        else:
            self._dataset['y_mean'] = None
            self._dataset['X_mean'] = None
            self._dataset['X_std'] = None
            self._dataset['is_sparse'] = None

        self._dataset['y_min'] = y_min if y_min else float(y.min())
        self._dataset['y_max'] = y_max if y_max else float(y.max())

        if categorical is None:
            # assume 0, but we really don't know in this case.
            self._dataset['num_categorical'] = 0
        else:
            self._dataset['num_categorical'] = int(np.sum(categorical))

        self._dataset['task'] = task
        if task == constants.Tasks.CLASSIFICATION:
            if num_classes is None:
                self._dataset['num_classes'] = len(np.unique(y))
            else:
                self._dataset['num_classes'] = num_classes
            self._dataset['class_labels'] = np.unique(y)
        elif task == constants.Tasks.REGRESSION:
            self._dataset['num_classes'] = None

        for k in self._dataset.keys():
            assert k in self.meta_fields, "%s is not in meta_fields" % k

        self._dataset['X'] = X
        self._dataset['y'] = y
        self._dataset['sample_weight'] = sample_weight
        self._dataset['sample_weight_valid'] = None
        self._dataset['sample_weight_test'] = None

    def parse_simple_train_validate(self,
                                    name,
                                    task,
                                    X, y,
                                    X_valid, y_valid,
                                    sample_weight=None,
                                    sample_weight_valid=None,
                                    num_classes=None,
                                    y_min=None,
                                    y_max=None,
                                    init_all_stats=True):
        """
        creates a ClientDataset processing the input data

        :param name:
        :param task: task type
        :param X: train data
        :param y: label
        :param sample_weight:
        :param X_valid: validation data
        :param y_valid: validation label
        :param sample_weight_valid:
        :param num_classes: number of classes in the experiment
        :param y_min: min value of the label
        :param y_max: max value of the label
        :return: a client dataset woth all metadata set.
        """
        if num_classes is None:
            num_classes = np.unique(np.concatenate(
                (np.unique(y), np.unique(y_valid)), axis=0)).shape[0]
        self._init_dataset(
            name, task, X, y, sample_weight=sample_weight,
            num_classes=num_classes, y_min=y_min, y_max=y_max,
            init_all_stats=init_all_stats)

        self._dataset['X_valid'] = X_valid
        self._dataset['y_valid'] = y_valid
        self._dataset["sample_weight"] = sample_weight
        self._dataset['sample_weight_valid'] = sample_weight_valid
        self._dataset['train indices'] = np.arange(X.shape[0])

        if self._dataset['task'] == constants.Tasks.REGRESSION:
            self._dataset['bin_info'] = self.get_bin_info(X_valid.shape[0], y)

    def parse_data(self, name, task, X, y, sample_weight=None,
                   categorical=None, seed=123, perc_test=0.1,
                   perc_valid=0.1, CV=10, cv_splits_indices=None,
                   openml_id=None, test_data=None, num_classes=None,
                   y_min=None, y_max=None, init_all_stats=True):
        """

        :param name:
        :param task: task type
        :param X: input data
        :param y: label
        :param sample_weight:
        :param categorical: is it categorical?
        :param seed: random seed to use in spliting data.
        :param perc_test: test set percent
        :param perc_valid: validation set percent
        :param CV: cross validation #
        :param cv_splits_indices: list of np arrays of train, valid indexes
        :param openml_id:
        :param test_data: test data to use instead of getting from X
        :param num_classes: number of classes in the experiment
        :param y_min: min value of the label
        :param y_max: max value of the label
        :return: a client dataset woth all metadata set.
        """
        # sanity check...
        if perc_test + perc_valid >= 1.0:
            raise ValueError("perc_test + perc_valid must be < 1.0")
        if CV is None:
            CV = 0

        self._init_dataset(name, task, X, y,
                           sample_weight=sample_weight,
                           categorical=categorical,
                           openml_id=openml_id,
                           num_classes=num_classes,
                           y_min=y_min, y_max=y_max,
                           init_all_stats=init_all_stats)

        N = X.shape[0]
        if cv_splits_indices:
            full_index = np.arange(N)
        else:
            np.random.seed(seed)
            full_index = np.random.permutation(N)

        # Split into train/test
        if test_data is None:
            remaining_ind = full_index[:int(N * (1 - perc_test))]
            test_ind = full_index[int(N * (1 - perc_test)):]
        else:
            remaining_ind = full_index
            # TODO Nicolo: Do these belong in "binary_fields"?
            self._dataset['X_test'] = test_data['X']
            self._dataset['y_test'] = test_data['y']
            test_ind = np.arange(test_data['y'].shape[0]) + N + 1

            # assert remaining_ind.shape[0] == int(N*(1-perc_test))
        # assert test_ind.shape[0] == int(N*(perc_test))
        assert np.intersect1d(remaining_ind, test_ind).shape[0] == 0

        if cv_splits_indices is not None:
            # check if the custon split is valid split.
            ClientDatasets._validiate_cv_splits(
                max_index=N, max_size=len(remaining_ind),
                cv_splits_indices=cv_splits_indices, test_index=test_ind)
            self._dataset['train CV splits'] = cv_splits_indices
            if task == constants.Tasks.REGRESSION:
                self._dataset['bin_info'] = self.get_bin_info(
                    np.min([len(split[1]) for split in cv_splits_indices]),
                    self._dataset['y'])
        elif CV > 0 and not perc_valid:
            # Generate CV splits
            np.random.seed(seed)
            kf = model_selection.KFold(n_splits=CV)
            splits = []
            for train_index, valid_index in kf.split(remaining_ind):
                splits.append(
                    (remaining_ind[train_index], remaining_ind[valid_index]))
                assert np.intersect1d(splits[-1][0], test_ind).shape[0] == 0
            self._dataset['train CV splits'] = splits
            if task == constants.Tasks.REGRESSION:
                self._dataset['bin_info'] = self.get_bin_info(
                    int(self._dataset['num_samples'] / CV),
                    self._dataset['y'])
        elif CV > 0 and perc_valid:
            np.random.seed(seed)
            splits = []
            remaining_size = len(remaining_ind)
            for i in range(CV):
                remaining_ind = remaining_ind[np.random.permutation(
                    remaining_size)]
                splits.append((
                    remaining_ind[:int(remaining_size * (1 - perc_valid))],
                    remaining_ind[int(remaining_size * (1 - perc_valid)):]))
                assert np.intersect1d(splits[-1][0], test_ind).shape[0] == 0
            self._dataset['train CV splits'] = splits
            if task == constants.Tasks.REGRESSION:
                self._dataset['bin_info'] = self.get_bin_info(
                    int(self._dataset['num_samples'] * perc_valid),
                    self._dataset['y'])

        # Split train in train and validation

        # TODO: Remove below legacy code and refactor/fix all the code paths
        # that rely on it (such as refit)
        if not perc_valid:
            perc_valid = 0.1
        n_remaining = len(remaining_ind)
        n_valid = int(perc_valid * N)
        n_train = n_remaining - n_valid
        np.random.seed(seed)
        shuffled_ind = np.random.permutation(remaining_ind)
        valid_ind = shuffled_ind[n_train:]
        train_ind = shuffled_ind[:n_train]

        assert np.intersect1d(train_ind, test_ind).shape[0] == 0
        assert np.intersect1d(valid_ind, test_ind).shape[0] == 0

        # TODO: get rid of spaces in dictionary keys...
        self._dataset['train indices'] = train_ind
        self._dataset['valid indices'] = valid_ind
        self._dataset['test indices'] = test_ind
        self._dataset['sample_weight'] = sample_weight
        if task == constants.Tasks.REGRESSION and \
                'bin_info' not in self._dataset:
            self._dataset['bin_info'] = self.get_bin_info(
                int(self._dataset['num_samples'] * perc_valid),
                self._dataset['y'])

    def get_bin_info(self, n_val, y_test):
        """
        creates dictionary y binned with points in y.
        :param n_val:  number of items
        :param y_test:  label to be binned.
        :return:
        """
        default_num_bins, min_points_per_bin, percentile,\
            extra_outlier_bins = 100, 10, 1, 2
        if int(n_val / default_num_bins) >= min_points_per_bin:
            num_bins_major_perc = default_num_bins
        else:
            num_bins_major_perc = int(n_val / min_points_per_bin) -\
                extra_outlier_bins
        num_bins = num_bins_major_perc + extra_outlier_bins
        first_bin_end, last_bin_start = np.percentile(
            y_test, [percentile, 100 - percentile])
        bin_dict = {'number_of_bins': num_bins, 'bin_starts': np.zeros(
            num_bins), 'bin_ends': np.zeros(num_bins)}
        bin_width_major_perc = (
            last_bin_start - first_bin_end) / num_bins_major_perc
        bin_dict['bin_starts'][0], bin_dict['bin_starts'][-1] = \
            y_test.min(), last_bin_start
        bin_dict['bin_ends'][0], bin_dict['bin_ends'][-1] = \
            first_bin_end, y_test.max()
        bin_dict['bin_starts'][1:num_bins - 1] = \
            [first_bin_end + x * bin_width_major_perc
             for x in range(num_bins_major_perc)]
        bin_dict['bin_ends'][1:num_bins -
                             1] = bin_dict['bin_starts'][2:num_bins]
        return bin_dict

    def get_subsampled_dataset(self, subsample_percent, force_resample=False):
        """

        :param original_dataset:
        :param subsample_percent:
        :return: Another ClientDatasets object that is a subsample.
        """
        assert subsample_percent > 0 and subsample_percent < 100

        if not force_resample and subsample_percent in self._subsample_cache:
            return self._subsample_cache[subsample_percent]

        subsample_frac = float(subsample_percent) / 100.0

        # shallow copy the dataset
        ret = ClientDatasets()
        ret._dataset = copy.copy(self._dataset)

        train_y = None
        if self.get_meta('task') == constants.Tasks.CLASSIFICATION:
            train_y = self._dataset['y'][self._dataset['train indices']]

        new_train_indices, _ = model_selection.train_test_split(
            self._dataset['train indices'],
            train_size=subsample_frac,
            stratify=train_y)

        ret._dataset['train indices'] = new_train_indices

        # for CV
        ret._dataset['train CV splits'] = copy.copy(
            self._dataset['train CV splits'])
        for i, item in enumerate(ret._dataset['train CV splits']):
            train, test = item
            original_n = len(train)
            subsample_n = int(original_n * subsample_frac)
            sub_train = train[:subsample_n]
            ret._dataset['train CV splits'][i] = (sub_train, test)

            assert subsample_n == len(ret._dataset['train CV splits'][i][0])
            assert original_n == len(self._dataset['train CV splits'][i][0])

        self._subsample_cache[subsample_percent] = ret

        return ret

    @staticmethod
    def _check_data(X, y, categorical=None, missing_data=False):
        """

        :param X:
        :param y:
        :param categorical:
        :param missing_data:
        :return:
        """
        if not missing_data:
            assert (isinstance(X, np.ndarray) and not np.any(
                np.isnan(X))) or scipy.sparse.issparse(X)

        if categorical is not None:
            assert X.shape[1] == len(
                categorical), ("there should be one categorical indicator "
                               "for each feature")

        assert not np.any(np.isnan(y)), "can't have any missing values in y"
        assert X.shape[0] == y.shape[0], "X and y should have the same shape"
        assert len(y.shape) == 2, "y should be a vector Nx1"
        assert y.shape[1] == 1, "y should be a vector Nx1"

    @staticmethod
    def _encode_data(X, y, categorical):
        """

        :param X:
        :param y:
        :param categorical:
        :return:
        """
        if np.any(categorical):
            enc = sklearn.preprocessing.OneHotEncoder(
                categorical_features=categorical)
            X = enc.fit_transform(X).todense()
        return X, y

    @staticmethod
    def get_dataset(
            name, X, y, task, sample_weight=None, missing_data=False,
            categorical=None, seed=123, perc_test=0.1, perc_valid=0.1, CV=10,
            cv_splits_indices=None, openml_id=None, y_min=None, y_max=None):
        """

        :param name:
        :param X:
        :param y:
        :param sample_weight:
        :param missing_data:
        :param categorical:
        :param task:
        :param seed:
        :param perc_test:
        :param perc_valid:
        :param CV:
        :param cv_splits_indices:
        :param openml_id:
        :param y_min:
        :param y_max:
        :return:
        """
        ClientDatasets._check_data(X, y, categorical, missing_data)
        if categorical is not None:
            X, y = ClientDatasets._encode_data(X, y, categorical)

        ret = ClientDatasets()
        ret.parse_data(
            name=name, task=task, X=X, y=y, sample_weight=sample_weight,
            categorical=categorical, seed=seed,
            perc_test=perc_test, perc_valid=perc_valid, CV=CV,
            cv_splits_indices=cv_splits_indices, openml_id=openml_id,
            y_min=y_min, y_max=y_max)
        return ret

    @staticmethod
    def _validiate_cv_splits(
            max_index, max_size,
            cv_splits_indices, test_index=None):
        """

        :param max_index:
        :param max_size:
        :param cv_splits_indices:
        :param test_index:
        :return:
        """
        for train, valid in cv_splits_indices:
            for item in [train, valid]:
                if np.max(item) >= max_index:
                    raise ValueError(
                        "train index or valid index is out of bound")
                if np.min(item) < 0:
                    raise ValueError(
                        "train index or valid index is out of bound")
                if len(np.unique(item)) != item.shape[0]:
                    raise ValueError(
                        "train index or valid index has duplicates")

            if len(train) + len(valid) > max_size:
                raise ValueError(
                    "train index or valid index can not exceed size {0}"
                    .format(max_size))
            if np.intersect1d(train, valid).shape[0] != 0:
                raise ValueError("train index  in cv split index and valid "
                                 "index have common values, cv-split indices "
                                 "should be disjoint")

            if test_index is not None and len(test_index) > 0:
                if np.intersect1d(train, test_index).shape[0] != 0:
                    raise ValueError("train index  in cv split index and "
                                     "test_index have common values, cv-split "
                                     "indices and test index should be "
                                     "disjoint")
                if np.intersect1d(valid, test_index).shape[0] != 0:
                    raise ValueError("validation index  in cv split index and "
                                     "test_index have common values cv-split, "
                                     "indices and test index should be "
                                     "disjoint")


if __name__ == '__main__':
    pass
