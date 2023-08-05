# Copyright (c) 2017 Microsoft Corporation.  All rights reserved.
"""Objects for communicating with the miro server."""
import copy
import json

import requests

from automl.client.core.common import (client_state, constants, pipeline_spec,
                                       problem_info, resource_limits)


class RecommendationResponse(object):

    def __init__(self,
                 p_spec,
                 predicted_cost=None,
                 predicted_status=None,
                 training_percent=None,
                 predicted_metrics=None,
                 pipeline_id=None):
        """
        Initializes a recommendation response object.

        Args:
            p_spec (PipelineSpec): pipeline specification
            predicted_cost (float): predicted cost
            predicted_status (string): predicted status code,
                see constants.ServerStatus
            training_percent (int): percentage of dataset to use for training
            predicted_metrics (dict of string and float):
                predicted metrics for the pipeline
            pipeline_id (PipelineID): id representing the pipeline,
                optional if pipeline_spec is specified
        """
        self.p_spec = p_spec
        self.predicted_cost = predicted_cost
        self.predicted_status = predicted_status
        self.training_percent = training_percent
        self.predicted_metrics = predicted_metrics
        self.pipeline_id = pipeline_id

    @staticmethod
    def from_pid(pipeline_id,
                 predicted_cost=None,
                 predicted_status=None,
                 training_percent=100,
                 predicted_metrics=None):
        """
        Helper method to create a recommendation response with pid.

        Args:
            pipeline_id (PipelineID): id representing the pipeline
            predicted_cost (float): predicted cost
            predicted_status (string): predicted status code,
                see constants.ServerStatus
            training_percent (int): percentage of dataset to use for training
            predicted_metrics (dict of string and float):
                predicted metrics for the pipeline
        """
        res = RecommendationResponse(
            None,
            predicted_cost=float(predicted_cost) if predicted_cost else None,
            predicted_status=predicted_status,
            training_percent=training_percent,
            predicted_metrics=predicted_metrics,
            pipeline_id=pipeline_id)
        return res

    @staticmethod
    def from_dict(d):
        ret = RecommendationResponse(None)
        ret.__dict__ = copy.deepcopy(d)
        ret.p_spec = pipeline_spec.PipelineSpec.from_dict(ret.p_spec)
        return ret

    def to_dict(self):
        d = copy.deepcopy(self.__dict__)
        d['p_spec'] = self.p_spec.to_dict()
        return d


class MiroServerAPI(object):

    def __init__(self,
                 endpoint,
                 model_name="default",
                 api_key=None,
                 settings_file=None,
                 logger=None):
        """
        Initializes the class for talking with the Miro server.
        :param endpoint:
        :param model_name:
        :param api_key:
        :param settings_file:
        :param logger:
        """

        self._log = logger

        self._endpoint = endpoint
        self._model_name = model_name
        self._api_key = api_key

    def _handle_response(self, url, req_data, r):
        if r.status_code != 200:
            request_dump = ("\n\r" + url + "\n\r" +
                            json.dumps(req_data, indent=4))
            error_str = "server responded with status %s" % r.status_code
            error_str += request_dump
            self._log and self._log.error(error_str)
            raise Exception(error_str)

        try:
            data = r.json()
        except Exception:
            data = None
        if data is None:
            request_dump = ("\n\r" + url + "\n\r" +
                            json.dumps(req_data, indent=4))
            error_str = "failed to parse server response"
            error_str += request_dump
            self._log and self._log.error(error_str)
            raise Exception(error_str)

        if 'error' in data:
            self._log and self._log.error(data['error'])
            raise Exception(data['error'])

        return data

    def _get_pipeline_request(self, problem_info, state):
        r = self._get_request()
        r.update({'state': state.to_dict()})
        r.update({'problem_info': problem_info.to_dict()})
        return r

    def _get_request(self):
        return {
            'api_key': self._api_key,
        }

    def next_pipeline(self, problem_info, state):
        """
        TODO: describe this function.
        :param acquisition_function:
        :param acquisition_param:
        :param state: A ClientState object.
        :param problem_info: A ProblemInfo object.
        :return:
        """
        url = self._endpoint + "/models/%s/next" % self._model_name
        data = self._get_pipeline_request(problem_info, state)
        # TODO: generate real certs (and remove verify=False)
        r = requests.post(url, json=data, headers={
                          'content-type': 'application/json'}, verify=False)
        responses = self._handle_response(url, data, r)
        return [RecommendationResponse.from_dict(resp) for resp in responses]

    def fetch_api_version(self):
        """
        TODO: describe this function.
        :return:
        """
        url = self._endpoint + "/version"
        data = self._get_request()
        r = requests.post(url, json=data, headers={
                          'content-type': 'application/json'}, verify=False)
        return self._handle_response(url, data, r)

    def fetch_model_info(self):
        """
        TODO: describe this function.
        :return:
        """
        url = self._endpoint + "/models/%s/info" % self._model_name
        data = self._get_request()
        r = requests.post(url, json=data, headers={
                          'content-type': 'application/json'}, verify=False)
        return self._handle_response(url, data, r)


class InMemoryServerAPI(MiroServerAPI):
    """Implements the API to a server object in memory instead of REST."""

    def __init__(self, server, api_version=None, package_version=None):
        """Initializes the class for talking with the Miro server."""
        super(InMemoryServerAPI, self).__init__(None, api_key=1234)
        self._server = server
        self._api_version = api_version
        self._package_version = package_version

    def next_pipeline(self, problem_info, state):
        data = self._get_pipeline_request(problem_info, state)

        responses = json.loads(self._server.model_next(data))
        return [RecommendationResponse.from_dict(resp) for resp in responses]

    def fetch_api_version(self):
        return {'api_version': self._api_version,
                'package_version': self._package_version}

    def fetch_model_info(self):
        return json.loads(self._server.model_info())


class O16nServerAPI(MiroServerAPI):

    def __init__(self,
                 endpoint,
                 api_key=None,
                 settings_file=None):
        super(O16nServerAPI, self).__init__(
            endpoint, model_name=None, api_key=api_key,
            settings_file=settings_file)

    @staticmethod
    def input_df_to_state(input_df):
        metric = input_df.get('metric')
        if metric is None:
            metric = 'default'

        task = input_df.get('task')

        # Construct input objects for miro brain from input df
        cl_state = client_state.ClientState(metric, task)
        ids = input_df.get('pipeline_ids')
        scores = input_df.get('scores')
        pred_times = input_df.get('predicted_times', [])
        act_times = input_df.get('actual_times', [])
        for i in range(len(ids)):
            cl_state.update(ids[i], {metric: scores[i]},
                            pred_times[i] if i < len(pred_times) else 0.0,
                            act_times[i] if i < len(act_times) else 0.0,
                            predicted_metrics=input_df.get('predicted_metrics',
                                                           None))

        problem_info_var = problem_info.ProblemInfo(
            dataset_samples=input_df.get('num_samples'),
            dataset_features=input_df.get('num_features'),
            dataset_classes=input_df.get('num_classes'),
            dataset_num_categorical=input_df.get('num_categorical'),
            num_recommendations=input_df.get('num_recommendations'),
            runtime_constraints={
                resource_limits.TIME_CONSTRAINT:
                input_df.get('time_constraint')},
            task=task, metric=metric,
            cost_mode=input_df.get(
                'cost_mode', constants.PipelineCost.COST_NONE),
            is_sparse=input_df.get('is_sparse_data', False))

        problem_info_var.set_cost_mode()

        return problem_info_var, cl_state

    # Need this to follow the schema.json in O16N image
    @staticmethod
    def state_to_input_df_json(pinfo, cl_state):
        return {"input_df": O16nServerAPI.state_to_input_df_dic(
            pinfo, cl_state)}

    @staticmethod
    def state_to_input_df_dic(pinfo, cl_state):
        return {
            'metric': pinfo.metric,
            'task': pinfo.task,
            'pipeline_ids': cl_state.pipeline_hashes(),
            'scores': cl_state.optimization_scores(),
            'predicted_times': cl_state._predicted_times,
            'actual_times': cl_state._actual_times,
            'num_recommendations': pinfo.num_recommendations,
            'cost_mode': pinfo.cost_mode,
            'num_samples': pinfo.dataset_samples,
            'num_features': pinfo.dataset_features,
            'num_classes': pinfo.dataset_classes,
            'num_categorical': pinfo.dataset_num_categorical,
            'time_constraint': pinfo.runtime_constraints[
                resource_limits.TIME_CONSTRAINT]}

    def next_pipeline(self, pinfo, cl_state):
        # add the bearer token header for O16N Communication
        headers = {'Authorization': 'Bearer ' +
                   str(self._api_key), 'content-type': 'application/json'}
        data = O16nServerAPI.state_to_input_df_json(pinfo, cl_state)

        url = self._endpoint

        r = requests.post(url, data=json.dumps(data), headers=headers)
        response = self._handle_response(url, data, r)

        # response from o16n server is already a dic without p_spec.
        return response

    def fetch_api_version(self):
        raise NotImplementedError()

    def fetch_model_info(self):
        raise NotImplementedError()
