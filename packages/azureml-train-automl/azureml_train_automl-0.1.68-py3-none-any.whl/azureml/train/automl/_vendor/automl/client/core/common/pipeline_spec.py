# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Pipeline spec that can instantiate and ser/des."""
import copy
import importlib
import inspect
import json

import numpy as np
import sklearn
from sklearn import linear_model, pipeline

from automl.client.core.common import constants, model_wrappers, tf_wrappers

PREPROC_NAME = 'preproc'
SKLEARN_NAME = 'sklearn'
TF_NAME = 'tf'
YTRANS_NAME = 'y_transformer'
ENSEMBLE_NAME = 'ensemble'

WRAPPERS_MODULE = 'automl.client.core.common.model_wrappers'


class ObjectSpec(object):
    """Metaobject for serialization and deserialization"""
    def __init__(self, spec_class, module, class_name,
                 *param_args, **param_kwargs):
        """Constructor for ObjectSpec"""
        self.spec_class = spec_class
        self.module = module
        self.class_name = class_name
        self.param_args = param_args
        self.param_kwargs = param_kwargs
        self.prepared_kwargs = {}

    @classmethod
    def from_dict(cls, d):
        """Deserializes an ObjectSpec from a dictionary
        :param cls: the class of the object to create
        :param d: the dictionary to deserialize
        :return: ObjectSpec for the dictionary
        """
        ret = cls(None, None)
        ret.__dict__ = copy.deepcopy(d)
        return ret

    def to_dict(self):
        """Serialize an ObjectSpec to a dictionary
        :return: the dictionary of ObjectSpec attributes
        """
        self.prepared_kwargs = {}
        d = copy.deepcopy(self.__dict__)
        return d

    def supports_constrained_fit(self):
        """Returns whether the pipeline step can stop given a time constraint
        Returns false for the ObjectSpec parent class
        """
        return False

    def prepare_kwargs(self, cls, problem_info,
                       random_state=None, num_threads=1):
        """Set self.prepared_kwargs, a modified copy of param_kwargs."""
        raise NotImplementedError()

    def instantiate(self, problem_info, random_state=None, num_threads=1):
        """Create a new object with additional parameters
        :param problem_info:
        :param random_state:
        :param num_threads:
        :return: a new object from the module and class from the constructor
        """
        mod = importlib.import_module(self.module)
        cls = getattr(mod, self.class_name)

        self.prepare_kwargs(cls, problem_info, random_state=random_state,
                            num_threads=num_threads)

        return cls(*self.param_args, **self.prepared_kwargs)


class PreprocessorObject(ObjectSpec):
    """Serializable pipeline preprocessing step"""
    def __init__(self, *args, **kwargs):
        """Constructor for PreprocessorObject"""
        super(PreprocessorObject, self).__init__(
            PREPROC_NAME, *args, **kwargs)

    def prepare_kwargs(self, cls, problem_info,
                       random_state=None, num_threads=1):
        """Saves parameters to be serialized
        :param problem_info:
        :param random_state:
        :param num_threads:
        """
        self.prepared_kwargs = copy.deepcopy(self.param_kwargs)


class SklearnObject(ObjectSpec):
    """Serializable pipeline model step"""
    def __init__(self, *args, **kwargs):
        """Constructor for SklearnObject"""
        super(SklearnObject, self).__init__(SKLEARN_NAME, *args, **kwargs)

    def prepare_kwargs(self, cls, problem_info,
                       random_state=None, num_threads=1):
        """Set self.prepared_kwargs, a modified copy of param_kwargs."""
        self.prepared_kwargs = copy.deepcopy(self.param_kwargs)
        argspec = inspect.getfullargspec(cls)
        if argspec.args:
            if 'random_state' in argspec.args:
                self.prepared_kwargs['random_state'] = random_state

            if 'n_jobs' in argspec.args:
                self.prepared_kwargs['n_jobs'] = num_threads


class TFObject(ObjectSpec):

    def __init__(self, *args, **kwargs):
        super(TFObject, self).__init__(TF_NAME, *args, **kwargs)

    def prepare_kwargs(self, cls, problem_info,
                       random_state=None, num_threads=1):
        """Set self.prepared_kwargs, a modified copy of param_kwargs."""
        self.prepared_kwargs = copy.deepcopy(self.param_kwargs)

        if random_state is not None:
            self.prepared_kwargs['seed'] = random_state

        if 'optimizer' in self.prepared_kwargs:
            opt_name = self.prepared_kwargs.pop('optimizer')
            if opt_name not in tf_wrappers.OPTIMIZERS:
                raise ValueError('Optimizer {0} not known.'.format(opt_name))

            if 'learning_rate' not in self.prepared_kwargs:
                raise ValueError('Optimizer requires learning rate.')

            if opt_name == 'momentum':
                opt = tf_wrappers.OPTIMIZERS[opt_name](
                    self.prepared_kwargs.pop('learning_rate'),
                    self.prepared_kwargs['momentum'])
            else:
                opt = tf_wrappers.OPTIMIZERS[opt_name](
                    self.prepared_kwargs.pop('learning_rate'))
            self.prepared_kwargs['optimizer'] = opt

            if 'momentum' in self.prepared_kwargs:
                self.prepared_kwargs.pop('momentum')

        self.prepared_kwargs['max_time'] = problem_info.get_time_constraint()

        if 'activation_fn' in self.prepared_kwargs:
            if (self.prepared_kwargs['activation_fn'] not in
                    tf_wrappers.ACTIVATION_FNS):
                raise ValueError('Unknown activation fn: {0}'.format(
                    self.prepared_kwargs['activation_fn']))
            self.prepared_kwargs['activation_fn'] = tf_wrappers.ACTIVATION_FNS[
                self.prepared_kwargs['activation_fn']]
        if problem_info.task == constants.Tasks.CLASSIFICATION:
            self.prepared_kwargs['n_classes'] = problem_info.dataset_classes

    def supports_constrained_fit(self):
        return True


class EnsembleObject(ObjectSpec):
    MODEL_KEY = 'models'
    CLF_KEY = 'clf'

    def __init__(self, **kwargs):
        super(EnsembleObject, self).__init__(
            ENSEMBLE_NAME, WRAPPERS_MODULE, 'EnsembleWrapper',
            **kwargs)

    @staticmethod
    def logistic_regression_to_json(lrmodel):
        data = {}
        data['init_params'] = lrmodel.get_params()
        data['model_params'] = mp = {}
        for p in ('coef_', 'intercept_', 'classes_', 'n_iter_'):
            mp[p] = getattr(lrmodel, p).tolist()
        return json.dumps(data)

    @staticmethod
    def logistic_regression_from_json(jstring):
        data = json.loads(jstring)
        model = linear_model.LogisticRegression(**data['init_params'])
        for name, p in data['model_params'].items():
            setattr(model, name, np.array(p))
        return model

    def prepare_kwargs(self, cls, problem_info,
                       random_state=None, num_threads=1):
        self.prepared_kwargs = copy.deepcopy(self.param_kwargs)
        # Turn object dicts into specs so they get passed to wrapper
        # as instantiated objects.
        self.prepared_kwargs[EnsembleObject.MODEL_KEY] = [
            PipelineSpec.from_dict(
                obj_dict).instantiate_pipeline_spec(
                    problem_info, random_state=random_state)
            for obj_dict in self.param_kwargs[EnsembleObject.MODEL_KEY]]
        self.prepared_kwargs[EnsembleObject.CLF_KEY] = (
            EnsembleObject.logistic_regression_from_json(
                self.prepared_kwargs[EnsembleObject.CLF_KEY]))


class PipelineSpec(object):
    """Serializable pipeline"""
    CLASS_MAP = {
        PREPROC_NAME: PreprocessorObject,
        SKLEARN_NAME: SklearnObject,
        TF_NAME: TFObject,
        YTRANS_NAME: PreprocessorObject,
        ENSEMBLE_NAME: EnsembleObject
    }

    def __init__(self, objects, pid):
        """Constructor for PipelineSpec
        :param objects: a list of ObjectSpecs
        :param pid: the pipeline ID
        """
        self.objects = objects
        self.pipeline_id = pid

    @staticmethod
    def from_dict(d):
        """Deserializes a PipelineSpec from a dictionary
        :param d: the dictionary to deserialize
        :return: the PipelineSpec created from d
        """
        objs = [PipelineSpec.CLASS_MAP[o['spec_class']].from_dict(o)
                for o in d['objects']]
        ret = PipelineSpec(objs, d['pipeline_id'])
        return ret

    def to_dict(self):
        """Serializes a PipelineSpec to a dictionary
        :return: the dictionary containing the steps of the pipeline serialized
            as dictionaries
        """
        d = copy.deepcopy(self.__dict__)
        d['objects'] = [o.to_dict() for o in self.objects]
        return d

    def class_strings(self):
        """Returns a list of class names for each step in the pipeline"""
        return [o.class_name for o in self.objects]

    def summary(self):
        """Returns a string representation of the pipeline (via class names)"""
        return '{ ' + ', '.join(self.class_strings()) + ' }'

    def supports_constrained_fit(self):
        """Indicates of the model can stop itself according to time
        constraint.  Currently implemented as an any(), which is just a
        concise way to find the model object.
        """
        return any([o.supports_constrained_fit() for o in self.objects])

    def instantiate_pipeline_spec(
            self, problem_info, random_state=None, is_sparse=False):
        """Creates a new PipelineSpec given extra parameters
        :param problem_info:
        :param random_state:
        :param num_threads:
        :return: a new PipelineSpec
        """
        # TODO: having a different pipeline class for ones with a y_transformer
        # is a bit ugly.
        objs = self.objects
        y_trans_objs = [o for o in self.objects if o.spec_class == YTRANS_NAME]
        if y_trans_objs:
            objs = [o for o in self.objects if o.spec_class != YTRANS_NAME]

        pipe = pipeline.Pipeline(
            [(obj.class_name, obj.instantiate(
                problem_info,
                random_state=random_state,
                num_threads=problem_info.num_threads))
                for obj in objs])

        if y_trans_objs:
            for ytrans in y_trans_objs:
                pipe = model_wrappers.PipelineWithYTransformations(
                    pipe, ytrans.class_name, ytrans.instantiate(
                        problem_info,
                        random_state=random_state,
                        num_threads=problem_info.num_threads))

        return pipe
