# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for selecting algorithms for AutoMLs ensembling feature"""
import logging
from collections import Counter

import numpy as np
from automl.client.core.common import metrics

from . import constants


class EnsembleSelector(object):
    """
    Ensembling Selection Algorithm following Caruana's Ensemble Selection from Library of Models paper
    """

    def __init__(self,
                 logger: logging.Logger,
                 fitted_models: list,
                 metric: str,
                 iterations: int = 10,
                 task_type: str = constants.Tasks.CLASSIFICATION):
        """Creates an EnsembleSelector used for choosing the pipelines that should be part of en ensemble

        Arguments:
            logger {logging.Logger} -- Logger instance
            fitted_models {list} -- A list of fitted pipelines
            metric {str} -- The metric that we're optimizing for during the selection algorithm

        Keyword Arguments:
            iterations {int} -- Number of iterations for Selection algorithm (default: {10})
            task_type {str} -- either classification or regression (default: {constants.Tasks.CLASSIFICATION})
        """
        # validate the task_type parameter to be within the supported range
        if task_type not in constants.Tasks.ALL:
            raise ValueError(
                "The task_type is not within th expected range ({0})"
                .format(constants.Tasks.ALL))

        # validate the input metric to optimize on
        if task_type == constants.Tasks.CLASSIFICATION and \
                metric in constants.Metric.CLASSIFICATION_SET:
            self.metric_objective = constants.MetricObjective.Classification[metric]
        elif task_type == constants.Tasks.REGRESSION and \
                metric in constants.Metric.REGRESSION_SET:
            self.metric_objective = constants.MetricObjective.Regression[metric]
        else:
            raise ValueError("The metric to optimize for, is not currently \
                            supported")

        if iterations < 1:
            raise ValueError("iterations parameter needs to be >=1")
        if logger is None:
            raise ValueError("logger parameter can not be None")

        self.fitted_models = fitted_models
        self.metric = metric
        self.iterations = iterations
        self.task_type = task_type
        self.model_count = len(fitted_models)
        self.logger = logger

    def select(self,
               X_valid: np.ndarray,
               y_valid: np.ndarray,
               sample_weight_valid: np.ndarray):
        """Selects the fitted pipelines that should be part of the Ensemble

        Arguments:
            X_valid {np.ndarray} -- The validation samples
            y_valid {np.ndarray} -- The target values for the sample dataset.
            sample_weight_valid {np.ndarray} -- The weights for the validation samples.
        """
        if X_valid is None or y_valid is None:
            raise ValueError("X_valid and y_valid are required parameters \
                for the EnsembleSelector.select() method")

        if self.iterations == 1:
            # short circuiting for the case of 1 iteration
            # so that we don't do any extra compute in the selection phases
            initial_size = 1
        else:
            initial_size = min(5, self.iterations // 2)

        self.logger.debug("Initial size {0}".format(initial_size))
        if self.task_type == constants.Tasks.CLASSIFICATION:
            num_classes = len(np.unique(y_valid))
        else:
            num_classes = 1
        predictions = self._compute_models_predictions(X_valid, num_classes)

        # prime the ensemble list with the models having the best scores
        single_model_scores = np.zeros(self.model_count)
        for i in range(self.model_count):
            single_model_scores[i] = self._get_model_score(num_classes,
                                                           predictions[:, :, i],
                                                           y_valid,
                                                           sample_weight_valid)
        self.logger.info(
            "Single models scores: {0}".format(single_model_scores))

        # need to sort the models based on their scores
        # then choose the best initial ones to start the ensemble with
        # the sorting is based on the scores and result represents
        # the indices that would result in a sorted array
        if self.metric_objective == constants.OptimizerObjectives.MAXIMIZE:
            # because sorting is done in ASC order,
            # we'll need to reverse the result first
            ensemble = np.argsort(single_model_scores)[
                ::-1][:initial_size].tolist()
        else:
            ensemble = np.argsort(single_model_scores)[:initial_size].tolist()

        # after priming the ensemble, we'll need to keep on adding
        # models to it until we reach the desired count
        number_of_models_needed = self.iterations - initial_size
        self.logger.debug("Starting to add more models to the ensemble. \
                            Current ensemble: {0}".format(ensemble))

        for iteration in range(number_of_models_needed):
            scores = np.zeros([self.model_count])
            for j, model in enumerate(self.fitted_models):
                # we'll temporarily add this model to the ensemble and will simulate
                # the overall score of the resulting ensemble
                ensemble.append(j)

                # slice the predictions array to only contain the predictions for the members of the ensemble
                temp = predictions[:, :, np.array(ensemble)]
                # now, get the predictions of the ensemble model
                temp_predictions = self._get_ensemble_predictions(
                    temp, X_valid)
                # get the score of this simulated ensemble
                scores[j] = self._get_model_score(num_classes,
                                                  temp_predictions,
                                                  y_valid,
                                                  sample_weight_valid)

                self.logger.debug("Iteration {0}. Simulating ensemble: {1} yielded score {2}"
                                  .format(iteration, ensemble, scores[j]))

                # remove this model from the ensemble and continue with another
                ensemble.pop()

            # after we've tried the end-score with each of the individual ensembles,
            # get the best one from this iteration
            best = self._choose_best_model_for_ensemble(
                scores, single_model_scores)

            ensemble.append(best)
            self.logger.debug("Iteration {0}, chosen ensemble: {1}, score :{2}"
                              .format(iteration, ensemble, scores[best]))

        weights = self._compute_weights(ensemble)
        self.logger.info(
            "Final ensemble: {0}. Weights: {1}".format(ensemble, weights))

        unique_ensemble = []
        for e in ensemble:
            if e not in unique_ensemble:
                unique_ensemble.append(e)
        unique_weights = [weights[i]
                          for i in unique_ensemble if weights[i] > 0]

        self.logger.info("Unique models IDs in the ensemble: {0}. Weights: {1}"
                         .format(unique_ensemble, unique_weights))
        return unique_ensemble, unique_weights

    def _choose_best_model_for_ensemble(self, ensemble_scores, single_model_scores):
        if self.metric_objective == constants.OptimizerObjectives.MAXIMIZE:
            # first we need to find what's the maximum score for the ensembles simulated
            maximum_score = np.nanmax(ensemble_scores)
            # then find the model indices that maximized the ensemble (there can be multiple)
            maximum_score_indices = np.where(
                ensemble_scores == maximum_score)[0]
            # if there are multiple single models, choose the best one (the one that has maximum individual score)
            best = maximum_score_indices[np.nanargmax(
                [single_model_scores[i] for i in maximum_score_indices])]
        else:
            # similarly if we need to minimize the score, do same thing but look for the minimum score
            minimum_score = np.nanmin(ensemble_scores)
            minimum_score_indices = np.where(
                ensemble_scores == minimum_score)[0]
            best = minimum_score_indices[np.nanargmin(
                [single_model_scores[i] for i in minimum_score_indices])]
        return best

    def _compute_models_predictions(self, X_valid, num_classes):
        # 3 dimensional array [validationSetSize, numberOfClasses, numberOfModels]
        predictions = np.zeros(
            (X_valid.shape[0], num_classes, self.model_count))
        for i, model in enumerate(self.fitted_models):
            if model is None:
                continue
            if hasattr(model, 'predict_proba'):
                predictions[:, :, i] = model.predict_proba(X_valid)
            else:
                # for regression models, we'll use predict method
                predictions[:, :, i] = model.predict(X_valid)[:, None]
        return predictions

    def _get_ensemble_predictions(self,
                                  predictions,
                                  X_valid):
        temp = predictions.mean(2)
        if self.task_type == constants.Tasks.CLASSIFICATION:
            temp /= temp.sum(1)[:, None]
        else:
            temp = temp[:, None]
        return temp

    def _get_model_score(self,
                         num_classes,
                         predictions,
                         y_valid,
                         sample_weight_valid):
        # compute scores on the predictions array slice corresponding to that model index
        if self.task_type == constants.Tasks.REGRESSION:
            y_pred = predictions[:, 0]
        else:
            y_pred = predictions

        all_metrics = metrics.compute_metrics(y_pred=y_pred,
                                              y_test=y_valid,
                                              sample_weight=sample_weight_valid,
                                              metrics=[self.metric],
                                              num_classes=num_classes,
                                              task=self.task_type)
        return all_metrics[self.metric]

    def _compute_weights(self, ensemble):
        # create a list with the count of occurrences of each model inside the ensemble : Tuple<modelIndex, count>
        occurrences = Counter(ensemble).most_common()
        weights = np.zeros(self.model_count, dtype=float)
        for occurrence_tuple in occurrences:
            weights[occurrence_tuple[0]] = float(
                occurrence_tuple[1]) / self.iterations

        return weights
