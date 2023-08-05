# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Utility methods for interacting with azureml.dataprep.
"""
import os
import json
import numpy as np

DATAPREP_INSTALLED = True
try:
    import azureml.dataprep as dprep
except ImportError:
    DATAPREP_INSTALLED = False


def try_retrieve_pandas_dataframe(dataflow):
    """
    param dataflow: the dataflow to retrieve
    type: azureml.dataprep.Dataflow
    return: the retrieved pandas dataframe, or the original dataflow value when it is of incorrect type
    """
    if not is_dataflow(dataflow):
        return dataflow
    df = dataflow.to_pandas_dataframe()
    return df.values


def try_retrieve_numpy_array(dataflow):
    """
    param dataflow: the single column dataflow to retrieve
    type: azureml.dataprep.Dataflow
    return: the retrieved numpy array, or the original dataflow value when it is of incorrect type
    """
    if not is_dataflow(dataflow):
        return dataflow
    df = dataflow.to_pandas_dataframe()
    return df[df.columns[-1]].values


def try_resolve_cv_splits_indices(cv_splits_indices):
    """
    param cv_splits_indices: the list of dataflow where each represents a set of split indices
    type: list(azureml.dataprep.Dataflow)
    return: the resolved cv_splits_indices, or the original passed in value when it is of incorrect type
    """
    if cv_splits_indices is None:
        return None
    cv_splits_indices_list = []
    for split in cv_splits_indices:
        if not is_dataflow(split):
            return cv_splits_indices
        else:
            is_train_list = try_retrieve_numpy_array(split)
            train_indices = []
            valid_indices = []
            for i in range(len(is_train_list)):
                if is_train_list[i] == 1:
                    train_indices.append(i)
                elif is_train_list[i] == 0:
                    valid_indices.append(i)
            cv_splits_indices_list.append([np.array(train_indices), np.array(valid_indices)])
    return cv_splits_indices_list


def save_dataflows_to_json(dataflow_dict):
    """
    param dataflow_dict: the dict with key as dataflow name and value as dataflow
    type: dict(str, azureml.dataprep.Dataflow)
    return: the JSON string representation of the packed Dataflows
    """
    dataflow_list = []
    for name in dataflow_dict:
        dataflow = dataflow_dict[name]
        if not is_dataflow(dataflow):
            continue
        dataflow_list.append(dataflow.set_name(name))

    if len(dataflow_list) == 0:
        return None

    pkg_json_str = dprep.Package(dataflow_list).to_json()
    return json.dumps(json.loads(pkg_json_str)).replace('"', '\\"')


def load_dataflows_from_json(dataprep_json):
    """
    param dataprep_json: the JSON string representation of the packed Dataflows
    type: str
    return: a dict with key as dataflow name and value as dataflow, or None if JSON is malformed
    """
    pkg = dprep.Package.from_json(dataprep_json)
    dataflow_dict = {}
    for dataflow in pkg.dataflows:
        dataflow_dict[dataflow.name] = dataflow
    return dataflow_dict


def is_dataflow(dataflow):
    """
    param dataflow:
    return: True if dataflow is of type azureml.dataprep.Dataflow
    """
    if not DATAPREP_INSTALLED or not isinstance(dataflow, dprep.Dataflow):
        return False
    return True
