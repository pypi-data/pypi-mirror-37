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

import dill
from pathlib import Path
from .run import Run
from .properties import PropertyManager
from contextlib import closing
from datetime import datetime
from jinja2 import Template
import maya


class Experiment:

    config_file = 'config.yml'
    root_key = 'experiment'
    dir_artifacts = 'artifacts'
    dir_experiments = 'experiments'
    runs_key = 'runs'

    def __init__(self, name, client):
        self._name = name
        self._client = client
        self._runs = []

        self._work_dir = Path.cwd() / self.dir_experiments / self.name
        self._work_dir.mkdir(parents=True, exist_ok=True)
        Path(self._work_dir / self.dir_artifacts).mkdir(parents=True, exist_ok=True)

        # Initialize config
        pm = PropertyManager()
        try:
            pm.load(str(self._work_dir / self.config_file))
        except FileNotFoundError:
            pm.set('meta', {'created': str(datetime.now())})

        self._config = pm

    @property
    def name(self):
        return self._name

    def start_run(self) -> Run:
        run = Run(self)
        self._runs.append(run)
        return run

    def save_run(self, run: Run):
        runs = self._config.get(self._config.join(self.root_key, self.runs_key)) or []
        runs.append(run.to_json())
        self._config.set(self._config.join(self.root_key, self.runs_key), runs)
        self._save_config()

        for name, artifact in run.artifacts.items():
            with closing(open(self.get_artifact_path(run, name), 'wb')) as f:
                dill.dump(artifact, f)

    def reset(self):
        self._config.remove_all()
        self._runs = []

    def set_pipeline(self, pipeline):
        self._config.set('pipeline', {'dataset': pipeline._ds.name, 'name': pipeline.name})
        self._save_config()

    def set_meta(self, prop, value):
        meta = self._config.get('meta')
        meta[prop] = value
        self._config.set('meta', meta)
        self._save_config()

    def runs(self):
        props = self._config
        runs = props.get(props.join(self.root_key, self.runs_key)) or []
        return [Run.from_json(r, self) for r in runs]

    def get_run(self, run_id: str):
        for r in self.runs():
            if r.id == run_id:
                return r
        return None

    def _save_config(self):
        self._config.save(self._work_dir / self.config_file)

    def load_artifact(self, run: Run, name: str, extension: str = 'pk'):
        artifact_file = self.get_artifact_path(run, name, extension)
        with closing(open(artifact_file, 'rb')) as f:
            return dill.load(f)

    def get_artifact_path(self, run: Run, name: str, extension: str = 'pk'):
        return self._work_dir / self.dir_artifacts / "{}_{}.{}".format(name, run.id, extension)

    def _repr_html_(self):
        runs = self.runs()

        template = """
                <style>
                    #table1 { 
                      border: solid thin; 
                      border-collapse: collapse; 
                    }
                    #table1 caption { 
                      padding-bottom: 0.5em; 
                    }
                    #table1 th, 
                    #table1 td { 
                      border: solid thin;
                      padding: 0.5rem 2rem;
                    }
                    #table1 td {
                      white-space: nowrap;
                    }
                    #table1 td { 
                      border-style: none solid; 
                      vertical-align: top; 
                    }
                    #table1 th { 
                      padding: 0.2em; 
                      vertical-align: middle; 
                      text-align: center; 
                    }
                    #table1 tbody td:first-child::after { 
                      content: leader(". "); '
                    }
                </style>
                <table id="table1">
                    <caption><b>Experiment:</b> {{name}}</caption>
                    <thead>
                    <tr>
                        <th rowspan="2">ID</th>
                        <th rowspan="2">Date</th>
                        <th rowspan="2">Took</th>
                        <th colspan="{{num_params}}" scope="colgroup">Params</th>
                        <th colspan="{{num_metrics}}" scope="colgroup">Metrics</th>
                    </tr>
                    <tr>
                        {% for param in param_names %}
                        <th>{{param}}</th>
                        {% endfor %}
                        {% for metric in metric_names %}
                        <th>{{metric}}</th>
                        {% endfor %}
                    </tr>
                    </thead>
                    <tbody>
                        {% for run in runs %}
                        <tr>
                        <td>{{run.id}}</td>
                        <td>{{maya(run.start_time)}}</td>
                        <td>{{'%.2f' % run.took}} s</td>
                        {% for param in param_names %}
                        <td>{{run.params.get(param, "&#x2011;")}}</td>
                        {% endfor %}
                        {% for metric in metric_names %}
                        <td>{{'%.6f' % run.metrics.get(metric, 0.0)}}</td>
                        {% endfor %}
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>"""

        num_params = 0
        num_metrics = 0
        param_names = set()
        metric_names = set()
        if len(runs) > 0:
            for one_run in runs:
                param_names.update(one_run.params.keys())
                num_params = len(param_names)
                metric_names.update(one_run.metrics.keys())
                num_metrics = len(metric_names)

        t = Template(template)
        return t.render(name=self.name, runs=runs, maya=maya.MayaDT, num_params=num_params,
                        param_names=sorted(list(param_names)),
                        num_metrics=num_metrics, metric_names=sorted(list(metric_names)))

    def display(self):
        from IPython.display import (display, HTML)
        display(HTML(self._repr_html_()))
