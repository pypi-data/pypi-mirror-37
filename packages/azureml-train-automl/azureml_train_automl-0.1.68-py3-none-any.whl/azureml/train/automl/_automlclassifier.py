# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Classifier wrapper for AutoMLBase object"""
from . import constants
from ._automlbase import _AutoMLBase
import logging


class _AutoMLClassifier(_AutoMLBase):
    """
    Client to run AutoML classification experiments on Azure Machine Learning platform
    """

    def __init__(
            self,
            experiment,
            primary_metric=constants.Metric.Accuracy,
            num_classes=None,
            **kwargs):
        """
        Constructor for the AutoMLClassifier
        :param experiment: The azureml.core experiment
        :param primary_metric: The metric you want to optimize the pipeline for
        :param num_classes: number of classes in you label data
        :param kwargs: dictionary of keyword args
        """

        super().__init__(experiment=experiment,
                         task_type=constants.Tasks.CLASSIFICATION,
                         primary_metric=primary_metric,
                         num_classes=num_classes,
                         **kwargs)
        self.start_experiment()
