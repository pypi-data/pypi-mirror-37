# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Computation of available metrics."""
import sys

import numpy as np
import scipy.interpolate
import scipy.stats as st
import sklearn.metrics
import sklearn.preprocessing

from automl.client.core.common import constants


def minimize_or_maximize(metric, task=None):
    """Selects the objective given a metric
    Some metrics should be minimized and some should be maximized
    :param metric: the name of the metric to look up
    :param task: string "classification" or "regression"
    :return: returns a string "maximize" or "minimize"
    """
    if task is None:
        reg_metrics = get_default_metric_with_objective(
            constants.Tasks.REGRESSION)
        if metric in reg_metrics:
            return reg_metrics[metric]
        class_metrics = get_default_metric_with_objective(
            constants.Tasks.CLASSIFICATION)
        if metric in class_metrics:
            return class_metrics[metric]
        msg = 'Could not find objective for metric "{0}"'.format(metric)
        raise ValueError(msg)
    return get_default_metric_with_objective(task)[metric]


def get_all_nan(task):
    """Creates a dictionary of metrics to values for the given task
    All metric values are set to nan initially
    :param task: string "classification" or "regression"
    :return: returns a dictionary of nans for each metric for the task.
    """
    metrics = get_default_metric_with_objective(task)
    return {m: np.nan for m in metrics}


def get_metric_ranges(task, for_assert_sane=False):
    minimums = get_min_values(task)
    maximums = get_max_values(task, for_assert_sane=for_assert_sane)
    return minimums, maximums


def get_worst_values(task, for_assert_sane=False):
    minimums, maximums = get_metric_ranges(
        task, for_assert_sane=for_assert_sane)
    metrics = get_default_metric_with_objective(task)
    _MAX = constants.OptimizerObjectives.MAXIMIZE
    bad = {m: minimums[m] if obj == _MAX else maximums[m]
           for m, obj in metrics.items()}
    return bad


def get_min_values(task):
    metrics = get_default_metric_with_objective(task)
    # 0 is the minimum for metrics that are minimized and maximized
    bad = {m: 0.0 for m, obj in metrics.items()}
    bad[constants.Metric.R2Score] = -10.0  # R2 is different, clipped to -10.0
    bad[constants.Metric.Spearman] = -1.0
    return bad


def get_max_values(task, for_assert_sane=False):
    metrics = get_default_metric_with_objective(task)
    _MAX = constants.OptimizerObjectives.MAXIMIZE
    bad = {m: 1.0 if obj == _MAX else sys.float_info.max
           for m, obj in metrics.items()}
    # so the assertions don't fail, could also clip metrics instead
    if not for_assert_sane:
        bad[constants.Metric.LogLoss] = 10.0
        bad[constants.Metric.NormRMSE] = 10.0
        bad[constants.Metric.NormRMSLE] = 10.0
        bad[constants.Metric.NormMeanAbsError] = 10.0
        bad[constants.Metric.NormMedianAbsError] = 10.0
    return bad


def assert_metrics_sane(metrics, task):
    """Asserts that the given metric values are same
    The metric values should not be worse than the worst possible values
    for those metrics given the objectives for those metrics
    :param task: string "classification" or "regression"
    """
    worst = get_worst_values(task, for_assert_sane=True)
    obj = get_default_metric_with_objective(task)
    for k, v in metrics.items():
        if not np.isscalar(v) or np.isnan(v):
            continue
        # This seems to vary a lot.
        if k == constants.Metric.ExplainedVariance:
            continue
        if obj[k] == constants.OptimizerObjectives.MAXIMIZE:
            assert v >= worst[k], (
                '{0} is not worse than {1} for metric {2}'.format(
                    worst[k], v, k))
        else:
            assert v <= worst[k], (
                '{0} is not worse than {1} for metric {2}'.format(
                    worst[k], v, k))


def get_default_metric_with_objective(task):
    """Gets the dictionary of metric -> objective for the given task
    :param task: string "classification" or "regression"
    :return: dictionary of metric -> objective
    """
    if task == constants.Tasks.CLASSIFICATION:
        return constants.MetricObjective.Classification

    elif task == constants.Tasks.REGRESSION:
        return constants.MetricObjective.Regression
    else:
        raise NotImplementedError


def get_default_metrics(task):
    """Gets the metrics supported for a given task as a list
    :param task: string "classification" or "regression"
    :return: a list of the default metrics supported for the task
    """
    return list(get_default_metric_with_objective(task).keys())


def compute_metrics(y_pred, y_test, metrics=None, num_classes=None,
                    task=constants.Tasks.CLASSIFICATION,
                    y_max=None, y_min=None, sample_weight=None):
    """Computes the metrics given the test data results
    :param y_pred: predicted value (in probability in case of classification)
    :param y_test: target value
    :param metrics: metric/metrics to compute
    :param num_classes: num of classes in case of classification
    :param task: ml task
    :param y_max: max label value in case of regression
    :param y_min: min label value in case of regression
    :param sample_weight:
    :return: returns a dictionary with metrics computed
    """

    if metrics is None:
        metrics = get_default_metrics(task)

    if task == constants.Tasks.CLASSIFICATION:
        return compute_metrics_classification(y_pred, y_test, metrics,
                                              num_classes=num_classes,
                                              sample_weight=sample_weight)
    elif task == constants.Tasks.REGRESSION:
        if y_min is None:
            y_min = np.min(y_test)
        if y_max is None:
            y_max = np.max(y_test)
            assert y_max > y_min
        return compute_metrics_regression(y_pred, y_test, metrics, y_max,
                                          y_min, sample_weight=sample_weight)
    else:
        raise NotImplementedError


def compute_metrics_classification(y_pred_probs, y_test, metrics,
                                   num_classes=None, sample_weight=None,
                                   class_labels=None):
    """Computes the metrics for a classification task
    :param y_pred_probs: probability predictions
    :param y_test: target value
    :param metrics: metric/metrics to compute
    :param num_classes: num of classes
    :param sample_weight:
    :return: returns a dictionary with metrics computed
    """
    if y_test.dtype == np.float32 or y_test.dtype == np.float64:
        # Assume that the task is set appropriately and that the data
        # just had a float label arbitrarily.
        y_test = y_test.astype(np.int64)

    # Some metrics use an eps of 1e-15 by default, which results in nans
    # for float32.
    if y_pred_probs.dtype == np.float32:
        y_pred_probs = y_pred_probs.astype(np.float64)

    if num_classes is None:
        num_classes = max(len(np.unique(y_test)), y_pred_probs.shape[1])

    if metrics is None:
        metrics = get_default_metrics(constants.Tasks.CLASSIFICATION)

    results = {}

    binarizer = sklearn.preprocessing.LabelBinarizer()
    y_test_bin = binarizer.fit_transform(y_test)
    y_pred_bin = np.argmax(y_pred_probs, axis=1)

    if num_classes is None:
        num_classes = max(len(np.unique(y_test)), len(np.unique(y_pred_bin)))

    if num_classes == 2:
        # if both classes probs are passed, pick the positive class probs as
        # binarizer only outputs single column
        y_pred_probs = y_pred_probs[:, 1]

    if class_labels is not None:
        y_test_binarized = sklearn.preprocessing.label_binarize(
            y_test, class_labels)
        y_test_labels = np.unique(y_test)
        if (len(class_labels) == 2):
            y_test_binarized2 = np.array([[0, 0]] * len(y_test_binarized))
            for i in range(len(y_test_binarized)):
                if y_test_binarized[i][0] == 0:
                    y_test_binarized2[i][0], y_test_binarized2[i][1] = 0, 1
                elif y_test_binarized[i][0] == 1:
                    y_test_binarized2[i][0], y_test_binarized2[i][1] = 1, 0
            y_test_binarized = y_test_binarized2

            y_pred_probs2 = []
            for prob in y_pred_probs:
                y_pred_probs2.append(np.array([prob, 1 - prob]))
            y_pred_probs2 = np.array(y_pred_probs2)
        else:
            y_pred_probs2 = y_pred_probs

    if constants.Metric.Accuracy in metrics:
        results[constants.Metric.Accuracy] = try_calculate_metric(
            score=sklearn.metrics.accuracy_score, y_true=y_test,
            y_pred=y_pred_bin, sample_weight=sample_weight)

    if constants.Metric.WeightedAccuracy in metrics:
        # accuracy weighted by number of elements for each class
        w = np.ones(y_test.shape[0])
        for idx, i in enumerate(np.bincount(y_test.ravel())):
            w[y_test.ravel() == idx] *= (i / float(y_test.ravel().shape[0]))
        results[constants.Metric.WeightedAccuracy] = try_calculate_metric(
            score=sklearn.metrics.accuracy_score,
            y_true=y_test,
            y_pred=y_pred_bin,
            sample_weight=w)

    if constants.Metric.NormMacroRecall in metrics:
        # this is what is used here
        # https://github.com/ch-imad/AutoMl_Challenge/blob/2353ec0
        # /Starting_kit/scoring_program/libscores.py#L187
        # for the AutoML challenge
        # https://competitions.codalab.org/competitions/2321
        # #learn_the_details-evaluation
        # This is a normalized macro averaged recall, rather than accuracy
        # https://github.com/scikit-learn/scikit-learn/issues/6747
        # #issuecomment-217587210
        # Random performance is 0.0 perfect performance is 1.0
        cmat = try_calculate_metric(
            sklearn.metrics.confusion_matrix, y_true=y_test,
            y_pred=y_pred_bin, sample_weight=sample_weight)
        if isinstance(cmat, float):
            results[constants.Metric.NormMacroRecall] = \
                constants.Defaults.DEFAULT_PIPELINE_SCORE
        else:
            R = 1 / num_classes
            cms = cmat.sum(axis=1)
            if cms.sum() == 0:
                results[constants.Metric.NormMacroRecall] = \
                    constants.Defaults.DEFAULT_PIPELINE_SCORE
            else:
                results[constants.Metric.NormMacroRecall] = max(
                    0.0,
                    (np.mean(cmat.diagonal() / cmat.sum(axis=1)) - R) /
                    (1 - R))

    if constants.Metric.BalancedAccuracy in metrics:
        classes = np.unique(y_test)
        bac = np.nanmean([try_calculate_metric(sklearn.metrics.roc_auc_score,
                                               y_true=(y_test == k),
                                               y_score=(y_pred_bin == k),
                                               sample_weight=sample_weight)
                          for k in classes])
        results[constants.Metric.BalancedAccuracy] = bac

    if constants.Metric.LogLoss in metrics:
        results[constants.Metric.LogLoss] = \
            try_calculate_metric(sklearn.metrics.log_loss, y_true=y_test,
                                 y_pred=y_pred_probs,
                                 labels=np.arange(0, num_classes),
                                 sample_weight=sample_weight)

    if constants.Metric.ConfusionMatrices in metrics:
        bac = np.nan
        try:
            if class_labels is not None:
                missing_labels = [
                    item for item in class_labels if item not in y_test_labels]
                cm = try_calculate_metric(
                    sklearn.metrics.confusion_matrix,
                    y_true=y_test, y_pred=y_pred_bin,
                    sample_weight=sample_weight)
                if len(missing_labels) != 0:
                    cm = _add_missing_labels_to_confusion_matrix(
                        cm, missing_labels, class_labels, y_test_labels)
                bac = cm
        except ValueError as e:
            bac = np.nan
        results[constants.Metric.ConfusionMatrices] = bac

        if constants.Metric.PrecisionRecall in metrics:
            bac = None
        try:
            if class_labels is not None:
                precision, recall = dict(), dict()
                for label in class_labels:
                    class_index = np.where(class_labels == label)[0][0]
                    label = str(label)
                    precision['class_' + label], recall['class_' + label], _ \
                        = _precision_recall_curve(
                        y_test_binarized[:, class_index],
                        y_pred_probs2[:, class_index])
                all_recall = np.unique(np.concatenate(
                    [recall['class_' + str(label)] for label in class_labels]))
                mean_precision = np.zeros_like(all_recall)
                for label in class_labels:
                    if label in y_test_labels:
                        label = str(label)
                        f = scipy.interpolate.interp1d(
                            recall['class_' + label],
                            precision['class_' + label],
                            kind='zero')
                        mean_precision += f(all_recall)
                mean_precision /= len(y_test_labels)
                precision['macro'] = mean_precision
                precision['micro'], recall['micro'], _ = \
                    _precision_recall_curve(
                        y_test_binarized.ravel(),
                        y_pred_probs2.ravel())
                recall['macro'] = all_recall
                bac = reformat_table(
                    {'precision': precision, 'recall': recall},
                    'precision',
                    'recall')
            else:
                bac = np.nan
        except ValueError as e:
            bac = np.nan
        results[constants.Metric.PrecisionRecall] = bac

    if constants.Metric.ROC in metrics:
        bac = None
        try:
            if class_labels is not None:
                false_positive_rate, true_positive_rate = dict(), dict()
                for label in class_labels:
                    class_index = np.where(class_labels == label)[0][0]
                    label = str(label)
                    false_positive_rate['class_' + label], \
                        true_positive_rate['class_' + label], _ = \
                        _roc_curve(
                            y_test_binarized[:, class_index],
                            y_pred_probs2[:, class_index])
                all_false_positive_rate = np.unique(np.concatenate(
                    [false_positive_rate['class_' + str(label)]
                     for label in class_labels]))
                mean_true_positive_rate = np.zeros_like(
                    all_false_positive_rate)
                for label in class_labels:
                    if label in y_test_labels:
                        label = str(label)
                        f = scipy.interpolate.interp1d(
                            false_positive_rate['class_' + label],
                            true_positive_rate['class_' + label],
                            kind='zero', fill_value="extrapolate")
                        mean_true_positive_rate += f(all_false_positive_rate)
                mean_true_positive_rate /= len(y_test_labels)
                true_positive_rate['macro'] = mean_true_positive_rate
                false_positive_rate['micro'], true_positive_rate['micro'], _ \
                    = _roc_curve(
                    y_test_binarized.ravel(),
                    y_pred_probs2.ravel())
                false_positive_rate['macro'] = all_false_positive_rate
                bac = reformat_table(
                    {'true_positive_rate': true_positive_rate,
                     'false_positive_rate': false_positive_rate},
                    'true_positive_rate',
                    'false_positive_rate')
            else:
                bac = np.nan
        except ValueError as e:
            bac = np.nan
        results[constants.Metric.ROC] = bac

    for m in metrics:
        if 'AUC' in m:
            results[m] = try_calculate_metric(
                sklearn.metrics.roc_auc_score, y_true=y_test_bin,
                y_score=y_pred_probs, average=m.replace('AUC_', ''),
                sample_weight=sample_weight)

        if 'f1_score' in m:
            results[m] = try_calculate_metric(
                sklearn.metrics.f1_score, y_true=y_test, y_pred=y_pred_bin,
                average=m.replace('f1_score_', ''),
                sample_weight=sample_weight)

        if 'precision_score' in m and 'average' not in m:
            results[m] = try_calculate_metric(
                sklearn.metrics.precision_score,
                y_true=y_test, y_pred=y_pred_bin,
                average=m.replace('precision_score_', ''),
                sample_weight=sample_weight)

        if 'recall_score' in m:
            results[m] = try_calculate_metric(
                sklearn.metrics.recall_score,
                y_true=y_test,
                y_pred=y_pred_bin,
                average=m.replace('recall_score_', ''),
                sample_weight=sample_weight)

        if 'average_precision_score' in m:
            results[m] = try_calculate_metric(
                sklearn.metrics.average_precision_score,
                y_true=y_test_bin,
                y_score=y_pred_probs,
                average=m.replace('average_precision_score_', ''),
                sample_weight=sample_weight)

    assert_metrics_sane(results, constants.Tasks.CLASSIFICATION)
    return results


def try_calculate_metric(score, **karg):
    """Calculates the metric given a metric calculation function
    :param score: an sklearn metric calculation function to score
    :return: the calculated score (or nan if there was an exception)
    """
    try:
        return score(**karg)
    except Exception as e:
        return constants.Defaults.DEFAULT_PIPELINE_SCORE


def _add_missing_labels_to_confusion_matrix(
        cm, missing_labels, class_labels, y_test_labels):
    count, cm = 0, cm.tolist()
    for missing_label in missing_labels:
        count += 1
        label_index = (class_labels.tolist()).index(missing_label)
        for row in cm:
            row.insert(label_index, 0)
        cm.insert(label_index, [0] * (len(y_test_labels) + count))
    return np.array(cm)


def confusion_matrices(matrix):
    """
    Calculate the normalized confusion matrix
    :param matrix: Confusion matrix
    :return:
        dictionary containing 'confusion_matrix' and
        'normalized_confusion_matrix'
    """
    try:
        if isinstance(matrix, float):
            return matrix
        normalized_matrix = []
        for row in matrix:
            normalized_row = []
            row_sum = np.sum(row)
            for cell in row:
                normalized_row = np.append(
                    normalized_row, cell / row_sum
                    if (row_sum != 0) else row_sum)
            normalized_matrix = np.append(normalized_matrix, [normalized_row])
        size = int(len(normalized_matrix) ** (0.5))
        normalized_matrix = np.reshape(normalized_matrix, (size, size))
        return {
            'confusion_matrix': matrix,
            'normalized_confusion_matrix': normalized_matrix}
    except Exception as e:
        return constants.Defaults.DEFAULT_PIPELINE_SCORE


def confusion_matrix_sums(matrices):
    """
    Get the sums of a confusion matrix
    :param matrices: Matrices to sum
    :return: Summed matrix
    """
    dim = len(matrices[0])
    all_sums = np.zeros((dim, dim))
    for i in range(dim):
        sums = np.zeros(dim)
        for j in range(len(matrices)):
            sums = np.add(sums, matrices[j][i])
        all_sums[i] = sums
    return all_sums


def _pr_or_roc_avg(dicts, yaxis, xaxis):
    all_xaxis, mean_yaxis, num_cross_vals = dict(), dict(), len(dicts)
    for key in dicts[0]:
        if xaxis in key:
            key_add = '_' if xaxis + '_macro' == key or \
                xaxis + '_micro' == key else '_class_'
            class_label = key.replace(xaxis + key_add, '')
            yaxis_label = yaxis + key_add + str(class_label)
            all_xaxis[key] = np.unique(np.concatenate(
                [dicts[i][key] for i in range(num_cross_vals)]))
            tmp = np.zeros_like(all_xaxis[key])
            for i in range(num_cross_vals):
                if not (np.isnan(dicts[i][key]).any() or
                        np.isnan(dicts[i][yaxis_label]).any()):
                    f = scipy.interpolate.interp1d(
                        dicts[i][key],
                        dicts[i][yaxis_label],
                        kind='zero',
                        fill_value="extrapolate")
                    tmp += f(all_xaxis[key])
            mean_yaxis[yaxis_label] = tmp / num_cross_vals
            all_xaxis[key], mean_yaxis[yaxis_label] = _curve_downsample(
                all_xaxis[key], mean_yaxis[yaxis_label])
    combined_dict = {**all_xaxis, **mean_yaxis}
    return combined_dict


def _precision_recall_curve(
        y_true, probas_pred, pos_label=None, sample_weight=None):
    precision, recall, thresholds = sklearn.metrics.precision_recall_curve(
        y_true, probas_pred, pos_label, sample_weight)
    recall, precision = _curve_downsample(recall, precision)
    return precision, recall, thresholds


def _roc_curve(
        y_true, y_score,
        pos_label=None, sample_weight=None, drop_intermediate=True):
    false_positive_rate, true_positive_rate, thresholds = \
        sklearn.metrics.roc_curve(
            y_true, y_score, pos_label, sample_weight, drop_intermediate)
    false_positive_rate, true_positive_rate = _curve_downsample(
        false_positive_rate, true_positive_rate)
    return false_positive_rate, true_positive_rate, thresholds


def _curve_downsample(x_values, y_values):
    max_num_samples = 1000
    if len(x_values) > max_num_samples:
        f = scipy.interpolate.interp1d(x_values, y_values, kind='zero')
        x_values = np.linspace(0, 1, num=max_num_samples)
        y_values = f(x_values)
    return x_values, y_values


def reformat_table(dictionary, yaxis, xaxis):
    """Convert x and y axis lists to a dictionary"""
    reformated_dict = dict()
    for label in dictionary[yaxis]:
        ykey, xkey = yaxis + '_' + str(label), xaxis + '_' + str(label)
        reformated_dict[xkey] = dictionary[xaxis][label]
        reformated_dict[ykey] = dictionary[yaxis][label]
    return reformated_dict


def compute_metrics_regression(
        y_pred, y_test, metrics, y_max, y_min,
        sample_weight=None, bin_info=None):
    """Computes the metrics for a regression task
    :param y_pred:
    :param y_test:
    :param metrics:
    :param y_max:
    :param y_min:
    :param y_pred: predicted value
    :param y_test: target value
    :param metrics: metric/metrics to compute
    :param y_max: max label value in case of regression
    :param y_min: min label value in case of regression
    :param sample_weight:
    :param bin_info: binning information for true values in case of regression
    :return: a dictionary with metrics computed
    """
    if y_min is None:
        y_min = np.min(y_test)
    if y_max is None:
        y_max = np.max(y_test)
        assert y_max > y_min
    if metrics is None:
        metrics = get_default_metrics(constants.Tasks.REGRESSION)

    results = {}

    # Regression metrics The scale of some of the metrics below depends on the
    # scale of the data. For this reason, we rescale it by the distance between
    # y_max and y_min. Since this can produce negative values we take the abs
    # of the distance https://en.wikipedia.org/wiki/Root-mean-square_deviation

    if constants.Metric.ExplainedVariance in metrics:
        bac = sklearn.metrics.explained_variance_score(
            y_test, y_pred, sample_weight=sample_weight,
            multioutput='uniform_average')
        results[constants.Metric.ExplainedVariance] = bac

    if constants.Metric.R2Score in metrics:
        bac = sklearn.metrics.r2_score(
            y_test, y_pred,
            sample_weight=sample_weight, multioutput='uniform_average')
        results[constants.Metric.R2Score] = np.clip(
            bac, constants.Metric.CLIPS_NEG[constants.Metric.R2Score], 1.0)

    if constants.Metric.Spearman in metrics:
        bac = st.spearmanr(y_test, y_pred)[0]
        results[constants.Metric.Spearman] = bac

        # mean AE
    if constants.Metric.MeanAbsError in metrics:
        bac = sklearn.metrics.mean_absolute_error(
            y_test, y_pred,
            sample_weight=sample_weight, multioutput='uniform_average')
        results[constants.Metric.MeanAbsError] = bac

    if constants.Metric.NormMeanAbsError in metrics:
        bac = sklearn.metrics.mean_absolute_error(
            y_test, y_pred,
            sample_weight=sample_weight, multioutput='uniform_average')
        bac = bac / np.abs(y_max - y_min)
        results[constants.Metric.NormMeanAbsError] = bac

    # median AE
    if constants.Metric.MedianAbsError in metrics:
        bac = sklearn.metrics.median_absolute_error(y_test, y_pred)
        results[constants.Metric.MedianAbsError] = bac

    if constants.Metric.NormMedianAbsError in metrics:
        bac = sklearn.metrics.median_absolute_error(y_test, y_pred)
        bac = bac / np.abs(y_max - y_min)
        results[constants.Metric.NormMedianAbsError] = bac

    # RMSE
    if constants.Metric.RMSE in metrics:
        bac = np.sqrt(
            sklearn.metrics.mean_squared_error(
                y_test, y_pred, sample_weight=sample_weight,
                multioutput='uniform_average'))
        results[constants.Metric.RMSE] = bac

    if constants.Metric.NormRMSE in metrics:
        bac = np.sqrt(
            sklearn.metrics.mean_squared_error(
                y_test, y_pred, sample_weight=sample_weight,
                multioutput='uniform_average'))
        bac = bac / np.abs(y_max - y_min)
        results[constants.Metric.NormRMSE] = np.clip(
            bac, 0,
            constants.Metric.CLIPS_POS.get(constants.Metric.NormRMSE, 100))

    # RMSLE
    if constants.Metric.RMSLE in metrics:
        bac = None
        try:
            bac = np.sqrt(
                sklearn.metrics.mean_squared_log_error(
                    y_test, y_pred, sample_weight=sample_weight,
                    multioutput='uniform_average')
            )
            bac = np.clip(
                bac, 0,
                constants.Metric.CLIPS_POS.get(constants.Metric.RMSLE, 100))
        except ValueError as e:
            bac = np.nan
        results[constants.Metric.RMSLE] = bac

    if constants.Metric.NormRMSLE in metrics:
        bac = None
        try:
            bac = np.sqrt(
                sklearn.metrics.mean_squared_log_error(
                    y_test, y_pred, sample_weight=sample_weight,
                    multioutput='uniform_average'))
            bac = bac / np.abs(y_max - y_min)
            bac = np.clip(
                bac, 0,
                constants.Metric.CLIPS_POS.get(
                    constants.Metric.NormRMSLE, 100))
        except ValueError as e:
            bac = np.nan
        results[constants.Metric.NormRMSLE] = bac

    if constants.Metric.Predictions in metrics:
        bac = None
        try:
            if bin_info is not None:
                num_bins = bin_info['number_of_bins']
                pred_indices_per_bin = [np.array([], dtype=int)] * (num_bins)
                predvtruedict = {
                    constants.Preds_Reg.TRUE_VALS_BINS_START:
                    bin_info['bin_starts'],
                    constants.Preds_Reg.TRUE_VALS_BINS_END:
                    bin_info['bin_ends'],
                    constants.Preds_Reg.AVG_PRED_VALS_PER_BIN:
                    np.zeros(num_bins),
                    constants.Preds_Reg.PRED_ERROR_PER_BIN:
                    np.zeros(num_bins),
                    constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN:
                    np.zeros(num_bins)}
                for i in range(len(y_test)):
                    for bin_index in range(len(bin_info['bin_ends'])):
                        if y_test[i] <= bin_info['bin_ends'][bin_index]:
                            pred_indices_per_bin[bin_index] = np.append(
                                pred_indices_per_bin[bin_index], int(i))
                            break
                predvtruedict[constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN] = \
                    np.array([len(x) for x in pred_indices_per_bin])
                predvtruedict[constants.Preds_Reg.AVG_PRED_VALS_PER_BIN] = \
                    np.array([
                        np.mean(y_pred[x])
                        if len(x) != 0
                        else 0 for x in pred_indices_per_bin])
                predvtruedict[constants.Preds_Reg.PRED_ERROR_PER_BIN] = \
                    np.array([(np.std(y_pred[x]) ** 2) * len(x)
                              if len(x) != 0 else 0
                              for x in pred_indices_per_bin])
                bac = predvtruedict
            else:
                bac = np.nan
        except ValueError as e:
            bac = np.nan
        results[constants.Metric.Predictions] = bac

    assert_metrics_sane(results, constants.Tasks.REGRESSION)
    return results


def _predvstrue_mean(dicts):
    num_cv, tot_bin_count = len(dicts), \
        len(dicts[0][
            constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN])
    predvtruedict = {
        constants.Preds_Reg.TRUE_VALS_BINS_START: np.zeros(tot_bin_count),
        constants.Preds_Reg.TRUE_VALS_BINS_END: np.zeros(tot_bin_count),
        constants.Preds_Reg.AVG_PRED_VALS_PER_BIN: np.zeros(tot_bin_count),
        constants.Preds_Reg.PRED_ERROR_PER_BIN: np.zeros(tot_bin_count),
        constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN: np.zeros(tot_bin_count)}
    for i in range(tot_bin_count):
        predvtruedict[constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN][i] = \
            np.sum(np.array(
                [dicts[j][constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN][i]
                 for j in range(num_cv)]))
        if predvtruedict[constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN][i] != 0:
            weighted_means_sum = np.sum(np.array(
                [dicts[j][constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN][i] *
                 dicts[j][constants.Preds_Reg.AVG_PRED_VALS_PER_BIN][i]
                 for j in range(num_cv)]))
            predvtruedict[constants.Preds_Reg.AVG_PRED_VALS_PER_BIN][i] = \
                weighted_means_sum \
                / predvtruedict[constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN][i]
            std_devs = np.sum(np.array([(
                dicts[j][constants.Preds_Reg.PRED_ERROR_PER_BIN][i] +
                dicts[j][constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN][i] *
                ((dicts[j][constants.Preds_Reg.AVG_PRED_VALS_PER_BIN][i] -
                  predvtruedict[constants.Preds_Reg.AVG_PRED_VALS_PER_BIN][
                    i]) **
                 2)
            ) for j in range(num_cv)]))

            predvtruedict[constants.Preds_Reg.PRED_ERROR_PER_BIN][i] = \
                ((std_devs) / predvtruedict[
                    constants.Preds_Reg.TRUE_VALS_COUNT_PER_BIN][i]) ** (0.5)
        else:
            predvtruedict[constants.Preds_Reg.AVG_PRED_VALS_PER_BIN][i] = 0
            predvtruedict[constants.Preds_Reg.PRED_ERROR_PER_BIN][i] = 0
    predvtruedict[constants.Preds_Reg.TRUE_VALS_BINS_START] = \
        dicts[0][constants.Preds_Reg.TRUE_VALS_BINS_START]
    predvtruedict[constants.Preds_Reg.TRUE_VALS_BINS_END] = \
        dicts[0][constants.Preds_Reg.TRUE_VALS_BINS_END]
    return predvtruedict
