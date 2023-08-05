# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Various constants used throughout AutoML."""

from automl.client.core.common.constants import (
    MODEL_PATH,
    Defaults,
    RunState,
    API,
    AcquisitionFunction,
    Status,
    PipelineParameterConstraintCheckStatus,
    OptimizerObjectives,
    Optimizer,
    Tasks,
    ClientErrors,
    ServerStatus,
    TimeConstraintEnforcement,
    PipelineCost,
    Metric,
    MetricObjective,
    TrainingType,
    NumericalDtype,
    TextOrCategoricalDtype,
    TrainingResultsType,
    Preds_Reg,
    get_metric_from_type,
    get_status_from_type
)


class SupportedAlgorithms:
    """Names for all algorithms supported by AutoML."""
    LogisticRegression = 'LogisticRegression'
    SGDClassifier = 'SGDClassifierWrapper'
    MultinomialNB = 'NBWrapper'
    BernoulliNB = 'NBWrapper'
    SupportVectorMachine = 'SVCWrapper'
    LinearSupportVectorMachine = 'LinearSVMWrapper'
    KNearestNeighborsClassifier = 'KNeighborsClassifier'
    DecisionTree = 'DecisionTreeClassifier'
    RandomForest = 'RandomForestClassifier'
    ExtraTrees = 'ExtraTreesClassifier'
    LightGBMClassifier = 'LightGBMClassifier'
    ElasticNet = 'ElasticNet'
    GradientBoostingRegressor = 'GradientBoostingRegressor'
    DecisionTreeRegressor = 'DecisionTreeRegressor'
    KNearestNeighborsRegressor = 'KNeighborsRegressor'
    LassoLars = 'LassoLars'
    SGDRegressor = 'SGDRegressor'
    RandomForestRegressor = 'RandomForestRegressor'
    ExtraTreesRegressor = 'ExtraTreesRegressor'
    # To be deprecated soon
    _KNN = 'kNN'
    _SVM = 'SVM'
    _KNNRegressor = 'kNN regressor'

    ALL = {
        LogisticRegression,
        SGDClassifier,
        MultinomialNB,
        BernoulliNB,
        SupportVectorMachine,
        LinearSupportVectorMachine,
        KNearestNeighborsClassifier,
        DecisionTree,
        RandomForest,
        ExtraTrees,
        LightGBMClassifier,
        ElasticNet,
        GradientBoostingRegressor,
        DecisionTreeRegressor,
        KNearestNeighborsRegressor,
        LassoLars,
        SGDRegressor,
        RandomForestRegressor,
        ExtraTreesRegressor,
        _KNN,
        _SVM,
        _KNNRegressor}


ENSEMBLE_PIPELINE_ID = "__AutoML_Ensemble__"

MAX_ITERATIONS = 1000
MAX_SAMPLES_BLACKLIST = 5000
MAX_SAMPLES_BLACKLIST_ALGOS = [SupportedAlgorithms.KNearestNeighborsClassifier,
                               SupportedAlgorithms.KNearestNeighborsRegressor,
                               SupportedAlgorithms.SupportVectorMachine,
                               SupportedAlgorithms._KNN,
                               SupportedAlgorithms._KNNRegressor,
                               SupportedAlgorithms._SVM]


Sample_Weights_Unsupported = {
    """Names of algorithms that do not support sample weights."""
    'Elastic net',
    'kNN',
    'Lasso lars',
    SupportedAlgorithms.ElasticNet,
    SupportedAlgorithms.KNearestNeighborsClassifier,
    SupportedAlgorithms.KNearestNeighborsRegressor,
    SupportedAlgorithms.LassoLars
}


Metric.CLASSIFICATION_SET = Metric.CLASSIFICATION_SET.union(
    {
        Metric.ConfusionMatrices,
        Metric.PrecisionRecall,
        Metric.ROC
    })
Metric.REGRESSION_SET.add(Metric.Predictions)
TrainingType.FULL_SET.remove(TrainingType.TrainValidateTest)


class ComputeTargets:
    """Names of compute targets supported by AutoML"""
    DSVM = 'VirtualMachine'
    BATCHAI = 'BatchAI'
