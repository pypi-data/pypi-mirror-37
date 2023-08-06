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

import sys
import yaml
import dill
import copy
from more_itertools import unique_everseen
from ds_discovery import Transition
from .utils import log_message
from .logger import getLogger
from .transition_ext import patch_tr

log = getLogger(__name__)


class Pipeline:

    """
    This class provides a pipeline abstraction used to transform data.  Pipeline steps are just Python functions that
    accept a DataFrame as an argument and are expected to transform or enrich the DataFrame for a certain goal.
    """

    def __init__(self, name: str, depends=None):
        self._name = name
        self._dependencies = []
        self._steps = []
        self._context = {}

        if depends is not None and len(depends) > 0:
            for d in depends:
                self.add_dependency(d)

    @property
    def name(self):
        return self._name

    @property
    def steps(self):
        return self._steps

    @property
    def dependencies(self):
        return self._dependencies

    def get_context(self, key: str, default_value=None):
        val = self._context.get(key)
        if val:
            return val
        else:
            depends = self._dependencies
            if len(depends) > 0:
                for dep in depends:
                    if self._name == dep._name:
                        raise Exception('Circular dependency detected in pipeline dependency graph')
                    val = dep.get_context(key)
                    if val:
                        return val

        return default_value

    def set_context(self, key: str, obj):
        self._context[key] = obj

    def add_step(self, fn, name=None):
        fn_name = fn.__name__
        if name is None:
            name = fn_name

        code = dill.dumps(fn, recurse=True)
        self._steps.append({'name': name, 'function': {'name': fn_name, 'code': code, 'type': 'inline'}})

        return self

    def get_step(self, name):
        for step in self._steps:
            if step.get('name') == name:
                code = step.get('function', {}).get('code')
                return dill.loads(code)
        return None

    def remove_step(self, name):
        new_steps = []
        for step in self._steps:
            if step.get('name') != name:
                new_steps.append(step)

        self._steps = new_steps

        return self

    def add_dependency(self, pipeline):
        self._dependencies.append(pipeline)
        self._dependencies = list(unique_everseen(self._dependencies))

        return self

    def reset(self, reset_deps=False, reset_context=False):
        self._steps = []
        if reset_deps:
            self._dependencies = []
        if reset_context:
            self._context = {}

        return self

    def from_pipeline(self, pipeline):
        self._steps = copy.deepcopy(pipeline.steps)
        self._dependencies = copy.deepcopy(pipeline.dependencies)
        self._context = copy.deepcopy(pipeline._context)
        return self

    def _run_dependencies(self, df=None):
        depends = self._dependencies
        if len(depends) > 0:
            for dep in depends:
                if self._name == dep._name:
                    raise Exception('Circular dependency detected in pipeline dependency graph')

                df = dep.run(data=df)

        return df

    def run(self, data):
        # run dependencies
        df = self._run_dependencies(data)

        log_message('running pipeline [%s]:' % self._name, log)

        for step in self._steps:
            func = step.get('function')
            if func is not None:
                if func.get('type', '').lower() == 'inline':
                    fn_name = func.get('name', 'unknown')
                    fn = dill.loads(func.get('code'))
                    log_message('> %s ' % fn_name, log)
                    result = fn(self, df)
                    if result is not None:
                        print("{}: {}".format(fn_name, result.shape))
                        df = result

        return df

    def dumps(self, stream=None, notebook=False):
        pipeline = {
            'steps': self._steps,
            'dependencies': [dep._name for dep in self._dependencies],
            'context': self._context
        }

        if stream is None and notebook:
            stream = sys.stdout

        s = yaml.dump({self._name: pipeline}, stream=stream, indent=2)
        if stream is None:
            return s


class DatasetPipeline:

    """
    Not meant to be directly instantiated by clients.

    This class provides a pipeline abstraction for use with Datasets. Pipeline steps are Python functions that
    accept a DataFrame as an argument and are expected to transform or enrich the DataFrame for a certain goal.
    Pipelines can be re-run on the raw source data to reproduce the data at the expected state.  The Pipeline
    configuration is persisted and can be shared with other users.
    """

    pipeline_key = 'pipeline'
    dependency_key = 'dependencies'
    steps_key = 'steps'
    context_key = 'context'

    def __init__(self, name: str, ds, tr: Transition, clear_cache=False, depends=None):
        self._name = name
        self._ds = ds

        # Add Transition extensions
        patch_tr(tr)

        # setup source cache
        if not tr.has_raw_file() or clear_cache:
            tr.save_raw_file(ds.as_pandas())

        # clear result cache
        if clear_cache:
            tr.remove_clean_file()

        self._contract = tr

        if depends is not None and len(depends) > 0:
            for d in depends:
                self.add_dependency(d)

    @property
    def name(self):
        return self._name

    @property
    def steps(self):
        dpm = self._contract.data_properties
        return dpm.get(dpm.join(dpm.contract_key, self.pipeline_key, self.steps_key)) or []

    @property
    def dependencies(self):
        dpm = self._contract.data_properties
        return dpm.get(dpm.join(dpm.contract_key, self.pipeline_key, self.dependency_key)) or []

    @property
    def _context(self):
        dpm = self._contract.data_properties
        return dpm.get(dpm.join(dpm.contract_key, self.pipeline_key, self.context_key)) or {}

    def get_context(self, key: str, default_value=None):
        dpm = self._contract.data_properties
        ctx = dpm.get(dpm.join(dpm.contract_key, self.pipeline_key, self.context_key)) or {}
        val = ctx.get(key)
        if val:
            return dill.loads(val)
        else:
            depends = self.dependencies
            if len(depends) > 0:
                for dep_name in depends:
                    if self._name == dep_name:
                        raise Exception('Circular dependency detected in pipeline dependency graph')

                    p = self._ds.pipeline(dep_name)
                    val = p.get_context(key, None)
                    if val:
                        return dill.loads(val)

        return default_value

    def set_context(self, key: str, obj, save=True):
        dpm = self._contract.data_properties
        ctx = dpm.get(dpm.join(dpm.contract_key, self.pipeline_key, self.context_key)) or {}
        ctx[key] = dill.dumps(obj)
        dpm.set(dpm.join(dpm.contract_key, self.pipeline_key, self.context_key), ctx)

        if save:
            self.save()

    def save(self):
        self._contract.save(True)

    def add_step(self, fn, name=None, save=True):
        fn_name = fn.__name__
        if name is None:
            name = fn_name

        code = dill.dumps(fn)

        dpm = self._contract.data_properties
        steps = dpm.get(dpm.join(dpm.contract_key, self.pipeline_key, self.steps_key)) or []
        steps.append({'name': name, 'function': {'name': fn_name, 'code': code, 'type': 'inline'}})
        dpm.set(dpm.join(dpm.contract_key, self.pipeline_key, self.steps_key), steps)

        if save:
            self.save()

        return self

    def get_step(self, name):
        dpm = self._contract.data_properties
        steps = dpm.get(dpm.join(dpm.contract_key, self.pipeline_key, self.steps_key))
        for step in steps:
            if step.get('name') == name:
                code = step.get('function', {}).get('code')
                return dill.loads(code)
        return None

    def remove_step(self, name, save=True):
        dpm = self._contract.data_properties
        steps = dpm.get(dpm.join(dpm.contract_key, self.pipeline_key, self.steps_key)) or []
        new_steps = []
        for step in steps:
            if step.get('name') != name:
                new_steps.append(step)

        dpm.set(dpm.join(dpm.contract_key, self.pipeline_key, self.steps_key), new_steps)

        if save:
            self.save()

        return self

    def add_dependency(self, pipeline_name, save=True):
        dpm = self._contract.data_properties
        deps = dpm.get(dpm.join(dpm.contract_key, self.pipeline_key, self.dependency_key)) or []
        deps.append(pipeline_name)
        dpm.set(dpm.join(dpm.contract_key, self.pipeline_key, self.dependency_key), list(unique_everseen(deps)))

        if save:
            self.save()

        return self

    def reset(self, reset_deps=False, reset_context=False, save=True):
        dpm = self._contract.data_properties
        dpm.set(dpm.join(dpm.contract_key, self.pipeline_key, self.steps_key), [])

        if reset_deps:
            dpm.set(dpm.join(dpm.contract_key, self.pipeline_key, self.dependency_key), [])

        if reset_context:
            dpm.set(dpm.join(dpm.contract_key, self.pipeline_key, self.context_key), {})

        if save:
            self.save()

        return self

    def from_pipeline(self, pipeline, save=True):
        dpm = self._contract.data_properties
        dpm.set(dpm.join(dpm.contract_key, self.pipeline_key, self.steps_key), pipeline.steps)
        dpm.set(dpm.join(dpm.contract_key, self.pipeline_key, self.dependency_key), pipeline.dependencies)
        dpm.set(dpm.join(dpm.contract_key, self.pipeline_key, self.context_key), pipeline._context)

        if save:
            self.save()

        return self

    def _run_dependencies(self, data=None, use_cache=True):
        dpm = self._contract.data_properties
        depends = dpm.get(dpm.join(dpm.contract_key, self.pipeline_key, self.dependency_key)) or []

        if len(depends) > 0:
            df = data
            for d in depends:
                if self._name == d:
                    raise Exception('Circular dependency detected in pipeline dependency graph')

                p = self._ds.pipeline(d, clear_cache=not(use_cache))
                df = p.run(data=df)

            return df

        else:
            return data

    def run(self, data=None, use_source_cache=True, use_cached_result=False, cache_result=False):
        if use_cached_result:
            try:
                return self._contract.load_clean_file()
            except:
                log.error('use_cached_result was True, but result cache could not be loaded')

        if data is not None:
            df = data
        elif use_source_cache:
            df = self._contract.load_raw_file()
        else:
            df = self._ds.as_pandas()

        # run dependencies
        df = self._run_dependencies(df, use_cache=use_source_cache)

        log_message('running pipeline [%s] for dataset [%s]:' % (self._name, self._ds.name), log)

        dpm = self._contract.data_properties
        steps = dpm.get(dpm.join(dpm.contract_key, self.pipeline_key, self.steps_key))
        for step in steps:
            func = step.get('function')
            if func is not None:
                if func.get('type', '').lower() == 'inline':
                    fn_name = func.get('name', 'unknown')
                    fn = dill.loads(func.get('code'))
                    log_message('> %s ' % fn_name, log)
                    result = fn(self, df)
                    if result is not None:
                        df = result

        if cache_result:
            self._contract.save_clean_file(df)

        return df

    def dumps(self, stream=None, notebook=False):
        dpm = self._contract.data_properties
        pipeline = dpm.get(dpm.join(dpm.contract_key, self.pipeline_key)) or {}

        if stream is None and notebook:
            stream = sys.stdout

        s = yaml.dump({self._name: pipeline}, stream=stream, indent=2)
        if stream is None:
            return s
