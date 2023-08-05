# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Regressor wrapper for AutoMLBase object"""
from . import constants
from ._automlbase import _AutoMLBase
import logging


class _AutoMLRegressor(_AutoMLBase):
    """
    Client to run AutoML regression experiments on Azure Machine Learning platform
    """

    def __init__(
            self,
            experiment,
            primary_metric=constants.Metric.NormRMSE,
            y_min=None,
            y_max=None,
            **kwargs):
        """
        Constructor for the AutomlRegressor
        :param experiment: The azureml.core experiment
        :param primary_metric: The metric you want to optimize the pipeline for
        :param y_min:
        :param y_max:
        :param kwargs: dictionary of keyword args
        """
        super().__init__(experiment=experiment,
                         task_type=constants.Tasks.REGRESSION,
                         primary_metric=primary_metric,
                         y_min=y_min,
                         y_max=y_max,
                         **kwargs)
        self.start_experiment()
