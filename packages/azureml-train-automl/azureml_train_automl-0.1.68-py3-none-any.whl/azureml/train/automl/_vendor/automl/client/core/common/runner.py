# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Class for running experiments."""
import copy
import datetime
import json
import signal
import time

import numpy as np
import scipy
import sklearn.metrics
import sklearn.preprocessing

from automl.client.core.common import constants
from automl.client.core.common import metrics as mt
from automl.client.core.common import resource_limits
from automl.client.core.common.constants import (Metric,
                                                 Sample_Weights_Unsupported,
                                                 Tasks, TrainingResultsType,
                                                 TrainingType)
from automl.client.core.common.resource_limits import (default_resource_limits,
                                                       safe_enforce_limits)


class ClientRunner(object):
    """
    Runner which encapsulates the fit() method for various AutoML models.
    """
    def __init__(self,
                 pipelines,
                 datasets,
                 metrics=None,
                 task=constants.Tasks.CLASSIFICATION):
        """
        :param pipelines:
        :param datasets:  A ClientDatasets object.
        :param metrics:
        :param runtime_constraints:
        :param task: string, 'classification' or 'regression'
        """

        assert task in ['classification', 'regression']
        self.task = task

        if metrics is None:
            metrics = mt.get_default_metrics(self.task)

        self.metrics = metrics
        self.pipelines = pipelines
        self.datasets = datasets

    def time_fit(self, m, X, y):
        """
        :param m:
        :param X:
        :param y:
        :return:
        """
        t = datetime.datetime.utcnow()  # time.process_time()
        m.fit(X, y.ravel())
        elapsed_time = datetime.datetime.utcnow() - t
        return elapsed_time.total_seconds()

    def _run_train_valid(self, dataset, pipeline_spec,
                         problem_info,
                         random_state=None):
        """
        :param dataset:
        :param pipeline_spec:
        :return:
        """
        num_classes = dataset.get_num_classes()
        m = pipeline_spec.instantiate_pipeline_spec(
            problem_info,
            random_state=random_state)
        X_train, y_train, _ = dataset.get_train_set()
        X_valid, y_valid, _ = dataset.get_valid_set()
        fit_time = self.time_fit(m, X_train, y_train)

        if self.task == constants.Tasks.CLASSIFICATION:
            y_pred_valid = m.predict_proba(X_valid)
        else:
            y_pred_valid = m.predict(X_valid)

        score_valid = mt.compute_metrics(
            y_pred_valid, y_valid, num_classes=num_classes,
            metrics=self.metrics, task=self.task, y_max=y_train.max(),
            y_min=y_train.min())
        return score_valid, fit_time, m

    def _run_train_full(self, dataset, pipeline_spec,
                        problem_info,
                        random_state=None):
        """
        :param dataset:
        :param pipeline_spec:
        :return:
        """
        num_classes = dataset.get_num_classes()
        m = pipeline_spec.instantiate_pipeline_spec(
            problem_info,
            random_state=random_state)
        X_train, y_train, _ = dataset.get_train_set()
        X_valid, y_valid, _ = dataset.get_valid_set()
        X_full = (
            scipy.sparse.vstack((X_train, X_valid))
            if scipy.sparse.issparse(X_train)
            else np.concatenate((X_train, X_valid)))
        y_full = np.concatenate((y_train, y_valid))
        fit_time = self.time_fit(m, X_full, y_full)
        if self.task == constants.Tasks.CLASSIFICATION:
            y_pred_full = m.predict_proba(X_full)
        else:
            y_pred_full = m.predict(X_full)
        score_full = mt.compute_metrics(
            y_pred_full, y_full, num_classes=num_classes,
            metrics=self.metrics, task=self.task, y_max=y_train.max(),
            y_min=y_train.min())
        return score_full, fit_time, m

    def _run_cv(self, dataset, pipeline_spec, problem_info,
                random_state=None):
        """
        :param dataset:
        :param pipeline_spec:
        :return:
        """
        num_classes, y_min, y_max = None, None, None
        scores = []
        fit_times = []
        models = []
        if self.task == constants.Tasks.CLASSIFICATION:
            num_classes = num_classes = dataset.get_num_classes()
        elif self.task == constants.Tasks.REGRESSION:
            y_min = dataset.get_meta('y_min')
            y_max = dataset.get_meta('y_max')

        for X_train, y_train, _, X_test, y_test, _ in dataset.get_CV_splits():
            if y_min is None:
                y_min = min(y_train.min(), y_test.min())
            if y_max is None:
                y_max = max(y_train.max(), y_test.max())
            m = pipeline_spec.instantiate_pipeline_spec(
                problem_info,
                random_state=random_state)
            fit_time = self.time_fit(m, X_train, y_train)
            if self.task == constants.Tasks.CLASSIFICATION:
                y_pred_test = m.predict_proba(X_test)
            else:
                y_pred_test = m.predict(X_test)
            scores.append(mt.compute_metrics(
                y_pred_test, y_test, num_classes=num_classes,
                metrics=self.metrics, task=self.task, y_max=y_max,
                y_min=y_min))
            fit_times.append(fit_time)
            models.append(m)
        return scores, fit_times, models

    def _run_cv_mean(self, dataset, pipeline_spec, problem_info,
                     cv_results=None,
                     random_state=False):
        """
        :param dataset:
        :param pipeline_spec:
        :param cv_results:
        :return:
        """
        if cv_results is None:
            scores, fit_times, models = self._run_cv(
                dataset, pipeline_spec, problem_info,
                random_state=random_state)
        else:
            scores, fit_times, models = cv_results

        mean_time = float(np.mean(fit_times))
        mean_scores = {}
        for k in self.metrics:
            split_results = []
            for score in scores:
                val = dict.get(score, k)
                if (val is not None):
                    split_results.append(val)
            if(len(split_results) > 0):
                mean_scores[k] = float(np.mean(split_results))
        mean_scores[constants.TrainingResultsType.TRAIN_TIME] = np.mean(
            [res[constants.TrainingResultsType.TRAIN_TIME]
             for res in scores])
        return mean_scores, mean_time, models

    def _run(self, dataset, pipeline_spec, problem_info, sets_to_run,
             subsample_percent=None,
             random_state=None, include_models=False):
        """
        :param dataset: A dataset generated by ClientDatasets.parse_data().
        :param pipeline_spec: A pipeline specification (obtained from the API).
        :param sets_to_run: Which experiment types to run (e.g. CV,
            train_valid, etc).
        :param subsample_percent: A multiple of 5 between 5 and 100, inclusive.
        :return: train, validation, and test scores for the experiments
            specified in sets_to_run.
        """
        results = {TrainingResultsType.MODELS: {}}

        training_percent = subsample_percent or problem_info.training_percent
        if training_percent is not None and training_percent < 100:
            # train on a subset of the training dataset.
            results[TrainingResultsType.TRAIN_PERCENT] = training_percent
            dataset = dataset.get_subsampled_dataset(training_percent)
        else:
            results[TrainingResultsType.TRAIN_PERCENT] = 100

        num_classes = dataset.get_num_classes()
        X_train, y_train, _ = dataset.get_train_set()

        if constants.TrainingType.TrainAndValidation in sets_to_run:
            results[TrainingResultsType.TRAIN_VALIDATE_STATUS] = 0
            try:
                score_full, train_time, m = self._run_train_valid(
                    dataset, pipeline_spec, problem_info,
                    random_state=random_state)
                results[TrainingResultsType.VALIDATION_METRICS] = score_full
                results[TrainingResultsType.MODELS][
                    constants.TrainingType.TrainAndValidation] = m
                results[TrainingResultsType.VALIDATION_METRICS][
                    TrainingResultsType.TRAIN_TIME] = train_time
            except ValueError as e:
                results[TrainingResultsType.TRAIN_VALIDATE_STATUS] = str(e)
                results[TrainingResultsType.VALIDATION_METRICS] = None

        if constants.TrainingType.TrainValidateTest in sets_to_run:
            results[TrainingResultsType.TRAIN_VALIDATE_STATUS] = 0
            try:
                score_full, train_time, m = self._run_train_valid(
                    dataset, pipeline_spec, problem_info,
                    random_state=random_state)
                results[TrainingResultsType.VALIDATION_METRICS] = score_full
                results[TrainingResultsType.MODELS][
                    constants.TrainingType.TrainValidateTest] = m

                if self.task == constants.Tasks.CLASSIFICATION:
                    y_pred_train = m.predict_proba(X_train)
                else:
                    y_pred_train = m.predict(X_train)

                results[TrainingResultsType.TRAIN_METRICS] = \
                    mt.compute_metrics(
                        y_pred_train, y_train, num_classes=num_classes,
                        metrics=self.metrics, task=self.task,
                        y_max=y_train.max(), y_min=y_train.min())
                results[TrainingResultsType.TRAIN_METRICS][
                    TrainingResultsType.TRAIN_TIME] = train_time

                X_test, y_test, _ = dataset.get_test_set()
                if self.task == constants.Tasks.CLASSIFICATION:
                    y_pred_test = m.predict_proba(X_test)
                else:
                    y_pred_test = m.predict(X_test)

                results[TrainingResultsType.TEST_METRICS] = \
                    mt.compute_metrics(
                        y_pred_test, y_test, num_classes=num_classes,
                        metrics=self.metrics, task=self.task,
                        y_max=y_train.max(), y_min=y_train.min())
            except ValueError as e:
                results[TrainingResultsType.TRAIN_VALIDATE_STATUS] = str(e)
                results[TrainingResultsType.VALIDATION_METRICS] = None
                results[TrainingResultsType.TRAIN_METRICS] = None
                results[TrainingResultsType.TEST_METRICS] = None

        if constants.TrainingType.TrainFull in sets_to_run:
            results[TrainingResultsType.TRAIN_FULL_STATUS] = 0
            try:
                score_full, train_time, m = self._run_train_full(
                    dataset, pipeline_spec, problem_info,
                    random_state=random_state)
                results[TrainingResultsType.MODELS][
                    constants.TrainingType.TrainFull] = m

                if self.task == constants.Tasks.CLASSIFICATION:
                    y_pred_train_full = m.predict_proba(X_train)
                else:
                    y_pred_train_full = m.predict(X_train)

                results[TrainingResultsType.TRAIN_FROM_FULL_METRICS] = (
                    mt.compute_metrics(
                        y_pred_train_full, y_train, num_classes=num_classes,
                        metrics=self.metrics, task=self.task,
                        y_max=y_train.max(), y_min=y_train.min()))
                results[TrainingResultsType.TRAIN_FROM_FULL_METRICS][
                    TrainingResultsType.TRAIN_TIME] = train_time

                if dataset.has_test_set():
                    X_test, y_test, _ = dataset.get_test_set()
                    if self.task == constants.Tasks.CLASSIFICATION:
                        y_pred_test_full = m.predict_proba(X_test)
                    else:
                        y_pred_test_full = m.predict(X_test)

                    results[TrainingResultsType.TEST_FROM_FULL_METRICS] = (
                        mt.compute_metrics(
                            y_pred_test_full, y_test, num_classes=num_classes,
                            metrics=self.metrics, task=self.task,
                            y_max=y_train.max(), y_min=y_train.min()))
            except ValueError as e:
                results[TrainingResultsType.TRAIN_FULL_STATUS] = str(e)
                results[TrainingResultsType.TRAIN_FROM_FULL_METRICS] = None
                results[TrainingResultsType.TEST_FROM_FULL_METRICS] = None

        if (constants.TrainingType.CrossValidation in sets_to_run):
            results[TrainingResultsType.CV_STATUS] = 0
            try:
                scores, fit_times, models = self._run_cv(
                    dataset, pipeline_spec, problem_info,
                    random_state=random_state)
                results[TrainingResultsType.MODELS][
                    constants.TrainingType.CrossValidation] = models
                for i in range(len(scores)):
                    score = scores[i]
                    fit_time = fit_times[i]
                    score[TrainingResultsType.TRAIN_TIME] = fit_time
                results[TrainingResultsType.CV_METRICS] = scores

                mean_scores, mean_time, models = self._run_cv_mean(
                    dataset, pipeline_spec, problem_info,
                    cv_results=(scores, fit_times, models))

                results[TrainingResultsType.CV_MEAN_METRICS] = mean_scores
            except ValueError as e:
                results[TrainingResultsType.CV_STATUS] = str(e)
                results[TrainingResultsType.CV_MEAN_METRICS] = None
                results[TrainingResultsType.CV_METRICS] = None

        if not include_models:
            del results[TrainingResultsType.MODELS]

        return results

    def _run_as_subprocess(self, fn, constraints, *args, **kwargs):
        pynobj = safe_enforce_limits(**constraints)
        result = pynobj(fn)(*args, **kwargs)
        return result, pynobj.exit_status

    def _run_in_process(self, fn, constraints, *args, **kwargs):
        return fn(*args, **kwargs), 0

    def _run_prewrap(self, fn, dataset, pipeline_spec, problem_info,
                     enforce_limits=True, **kwargs):
        """Handles clearing the constraints if needed and selecting
        to run in a subprocess or not.
        """
        c = problem_info.runtime_constraints
        if pipeline_spec.supports_constrained_fit():
            c = resource_limits.default_resource_limits
            enforce_limits = False

        args = (dataset, pipeline_spec, problem_info)
        wrapper = (self._run_as_subprocess if enforce_limits else
                   self._run_in_process)
        return wrapper(fn, c, *args, **kwargs)

    def run(self, dataset, pipeline_spec, problem_info, sets_to_run=None,
            subsample_percent=None, enforce_limits=True,
            new_constraints=None,
            random_state=None, include_models=False):
        """
        :param dataset:
        :param pipeline_spec:
        :param sets_to_run:
        :param subsample_percent:
        :param enforce_limits:  If true, run in a subprocess.
        :return: A tuple of:
            - a dict of results, filled in with TrainingResultsType keys.
            - a status from the subprocess enforcing constraints.
        """
        if sets_to_run is None:
            sets_to_run = list(constants.TrainingType.FULL_SET)

        kwargs = {'sets_to_run': sets_to_run,
                  'subsample_percent': subsample_percent,
                  'random_state': random_state,
                  'include_models': include_models}
        return self._run_prewrap(
            self._run, dataset, pipeline_spec, problem_info,
            enforce_limits=enforce_limits, **kwargs)


if __name__ == '__main__':
    pass
