"""
Copyright 2018 Cognitive Scale, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import numpy as np
import cuid
import io
import dill
from .timer import Timer
from cortex_client import ExperimentClient


class Run:

    def __init__(self, experiment):
        self._id = cuid.slug()
        self._experiment = experiment
        self._timer = None
        self._start = None
        self._end = None
        self._interval = None
        self._params = {}
        self._metrics = {}
        self._artifacts = {}
        self._meta = {}

    def start(self):
        if self._timer is not None:
            raise ValueError('Attempt to start a Run that is already started')

        self._timer = Timer()
        self._timer.start()
        self._start = self._timer.start_time

    def stop(self):
        self._timer.stop()
        self._end = self._timer.end_time
        self._interval = self._timer.interval
        self._experiment.save_run(self)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    @property
    def id(self):
        return self._id

    @property
    def start_time(self):
        return int(self._start)

    @property
    def end_time(self):
        return int(self._end)

    @property
    def took(self):
        return self._interval

    @property
    def params(self):
        return self._params

    def get_param(self, param):
        return self.params.get(param)

    @property
    def metrics(self):
        return self._metrics

    def get_metric(self, metric):
        return self.metrics.get(metric)

    @property
    def meta(self):
        return self._meta

    def get_meta(self, meta):
        return self.meta.get(meta)

    @property
    def artifacts(self):
        """
        The artifacts stored in this run.
        :return: the artifact object
        """
        return self._artifacts

    def get_artifact(self, name):
        """
        Get an artifact object by name.
        :param name: the key of the artifact
        :return: the artifact object
        """
        return self.artifacts.get(name)

    def to_json(self):
        doc = {'id': self.id, 'start': self.start_time, 'end': self.end_time, 'took': self.took,
               'params': self.params, 'metrics': self.metrics, 'meta': self.meta,
               'artifacts': [name for name in self.artifacts.keys()]}
        return doc

    @staticmethod
    def from_json(json, experiment):
        run = Run(experiment)
        run._id = json['id']
        run._start = json.get('start')
        run._end = json.get('end')
        run._interval = json.get('took')
        run._params = json.get('params', {})
        run._metrics = json.get('metrics', {})
        run._meta = json.get('meta', {})

        artifacts = json.get('artifacts', [])
        for name in artifacts:
            run._artifacts[name] = experiment.load_artifact(run, name)

        return run

    def log_param(self, name: str, param):
        _val = param

        if self._is_numpy_dtype(param):
            _val = np.asscalar(param)
        elif hasattr(param, 'tolist'):
            _val = param.tolist()

        self._params[name] = _val

    def log_params(self, params):
        for k, v in params.items():
            self.log_param(k, v)

    def log_metric(self, name: str, metric):
        _val = metric

        if self._is_numpy_dtype(metric):
            _val = np.asscalar(metric)
        elif hasattr(metric, 'tolist'):
            _val = metric.tolist()

        self._metrics[name] = _val

    def set_meta(self, name: str, val):
        _val = val

        if self._is_numpy_dtype(_val):
            _val = np.asscalar(_val)
        elif hasattr(_val, 'tolist'):
            _val = _val.tolist()

        self._meta[name] = _val

    def log_artifact(self, name: str, artifact):
        self._artifacts[name] = artifact

    def log_artifact_ref(self, name: str, ref):
        self.log_artifact(name, {'ref': ref})

    @staticmethod
    def _is_numpy_dtype(x):
        return hasattr(x, 'dtype')


class RemoteRun(Run):

    def __init__(self, experiment, client: ExperimentClient):
        super().__init__(experiment)
        self._client = client

    @staticmethod
    def create(experiment, client: ExperimentClient):
        r = client.create_run(experiment.name)
        run = RemoteRun(experiment, client)
        run._id = r['runId']

        return run

    @staticmethod
    def get(experiment, run_id, client: ExperimentClient):
        r = client.get_run(experiment.name, run_id)
        return RemoteRun.from_json(r, experiment)

    @staticmethod
    def from_json(json, experiment):
        run = RemoteRun(experiment, experiment._client)
        run._id = json['runId']
        run._start = json.get('start')
        run._end = json.get('end')
        run._interval = json.get('took')
        run._params = json.get('params', {})
        run._metrics = json.get('metrics', {})
        run._meta = json.get('meta', {})
        run._artifacts = json.get('artifacts', {})

        return run

    def log_param(self, name: str, param):
        super().log_param(name, param)
        self._client.update_param(self._experiment.name, self.id, name, param)

    def log_metric(self, name: str, metric):
        super().log_metric(name, metric)
        self._client.update_metric(self._experiment.name, self.id, name, metric)

    def set_meta(self, name: str, val):
        super().set_meta(name, val)
        self._client.update_meta(self._experiment.name, self.id, name, val)

    def log_artifact(self, name: str, artifact):
        super().log_artifact(name, artifact)
        if hasattr(artifact, 'ref'):
            with open(artifact['ref'], 'rb') as stream:
                self._client.update_artifact(self._experiment.name, self.id, name, stream)
        else:
            stream = io.BytesIO()
            dill.dump(artifact, stream)
            self._client.update_artifact(self._experiment.name, self.id, name, stream)

    def get_artifact(self, name):
        return self._client.get_artifact(self._experiment.name, self.id, name)
