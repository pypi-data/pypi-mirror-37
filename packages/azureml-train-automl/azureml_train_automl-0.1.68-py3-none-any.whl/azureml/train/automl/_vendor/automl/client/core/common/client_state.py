# Copyright (c) 2017 Microsoft Corporation.  All rights reserved.
import copy

import numpy as np

from automl.client.core.common import constants
from automl.client.core.common import metrics


class ClientState(object):
    """Tracks the history of a client's optimization loop."""

    def __init__(self, metric, task):
        self._scores = []
        self._pipeline_ids = []
        self._training_percentages = []
        self._predicted_times = []
        self._predicted_metrics = []
        self._actual_times = []
        self._metric = metric
        self._task = task

    @staticmethod
    def from_dict(d):
        d_copy = copy.deepcopy(d)  # copy first to avoid changing input
        d_copy['_scores'] = [{d_copy['_metric']: x} for x in d_copy['_scores']]
        ret = ClientState(None, None)  # args set later
        ret.__dict__ = d_copy
        return ret

    def to_dict(self):
        d = copy.deepcopy(self.__dict__)
        # Don't send all the scores, just the ones being optimized.
        d['_scores'] = self.optimization_scores()
        return d

    def pipeline_hashes(self):
        return self._pipeline_ids

    def _clip(self, score):
        if (self._metric in constants.Metric.CLIPS_POS or
                self._metric in constants.Metric.CLIPS_NEG):
            score = np.clip(
                score,
                constants.Metric.CLIPS_NEG.get(self._metric, None),
                constants.Metric.CLIPS_POS.get(self._metric, None))
        return score

    def optimization_scores(self, clip=True):
        """Return a list of scores for the metric being optimized."""
        vals = [float(x[self._metric]) for x in self._scores]
        if clip:
            vals = [self._clip(x) for x in vals]
        return vals

    def all_scores(self):
        return self._scores

    def all_predicted_metrics(self):
        return self._predicted_metrics

    def training_times(self):
        """Return a tuple of (predicted times, actual times)."""
        return (self._predicted_times, self._actual_times)

    def update(self, pid, score, predicted_time, actual_time,
               predicted_metrics=None, training_percent=100):
        """Add a new pipeline result.

        :param pid: Pipeline id (hash).
        :param score: A dict of results from validation set.
        :param predicted_time: The pipeline training time predicted
            by the server.
        :param actual_time: The actual pipeline training time.
        :param predicted_metrics: A dict of string to flow representing
            the predicted metrics for the pipeline
        :param training_percent: The training percent that was used.
        """
        self._scores.append(score)
        self._pipeline_ids.append(pid)
        if predicted_time is not None:
            self._predicted_times.append(predicted_time)

        self._predicted_metrics.append(predicted_metrics)
        self._actual_times.append(actual_time)
        self._training_percentages.append(training_percent)

    def get_best_pipeline_index(self):
        if np.isnan(self.optimization_scores()).all():
            return None
        objective = metrics.minimize_or_maximize(self._metric, self._task)
        if objective == 'maximize':
            return np.nanargmax(self.optimization_scores())
        else:
            return np.nanargmin(self.optimization_scores())

    def get_cost_stats(self):
        ret = {}
        if self._actual_times:
            ret['avg_pipeline_time'] = np.mean(self._actual_times)

        if self._predicted_times and self._actual_times:
            errors = (np.array(self._predicted_times) -
                      np.array(self._actual_times))
            ret['RMSE'] = np.sqrt(np.mean(np.square(errors)))
            ret['errors'] = errors.tolist()

        return ret
