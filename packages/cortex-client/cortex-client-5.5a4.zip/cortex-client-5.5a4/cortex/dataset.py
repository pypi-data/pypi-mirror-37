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

from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from cortex_client import DatasetsClient
from ds_discovery import Transition
from ds_discovery.transition.discovery import Visualisation, DataDiscovery
from .logger import getLogger
from .camel import CamelResource
from .transition_ext import patch_tr
from .utils import log_message
from .pipeline import Pipeline
from .pipeline_loader import PipelineLoader

log = getLogger(__name__)


class _Viz:

    """
    Not meant to be directly instantiated by clients.

    A simple wrapper that makes it easy to run multiple commonly used visualizations on the same DataFrame.
    """

    def __init__(self, df, figsize=(18, 9)):
        self.df = df
        self.corr_m = df.corr()

        if figsize is None or not isinstance(figsize, tuple):
            self.figsize = (18, 9)
        else:
            self.figsize = figsize

    def show_corr(self, column: str):
        cm_sorted = self.corr_m[column].sort_values(ascending=False)
        plt.rcParams['figure.figsize'] = self.figsize
        plt.xticks(rotation=90)
        sns.barplot(x=cm_sorted.index, y=cm_sorted)
        plt.show()
        plt.clf()

    def show_corr_heatmap(self, **kwargs):
        plt.rcParams['figure.figsize'] = self.figsize
        sns.heatmap(self.corr_m, annot=True, cmap=kwargs.get('cmap', 'BuGn'), robust=True, fmt=kwargs.get('fmt', '.1f'))
        plt.show()
        plt.clf()

    def show_missing(self):
        Visualisation.show_missing(df=self.df, figsize=self.figsize)

    def show_dist(self, column: str):
        try:
            from scipy.stats import norm
            fit = norm
        except ImportError:
            fit = None

        plt.rcParams['figure.figsize'] = self.figsize
        sns.distplot(self.df[column], fit=fit)
        plt.show()
        plt.clf()

    def show_probplot(self, column: str):
        try:
            from scipy import stats
            plt.rcParams['figure.figsize'] = self.figsize
            stats.probplot(self.df[column], plot=plt)
            plt.show()
            plt.clf()
        except ImportError:
            raise Exception('show_probplot requires SciPy to be installed')

    def show_corr_pairs(self, column: str, threshold=0.7):
        cm = self.df.corr()
        values = list(cm[column].values)
        keys = list(cm[column].keys())
        vars = [i for i in keys if values[keys.index(i)] > threshold]

        plt.rcParams['figure.figsize'] = self.figsize
        sns.pairplot(self.df, height=3, vars=vars)
        plt.show()
        plt.clf()


class _DatasetPipelineLoader(PipelineLoader):

    def __init__(self, ds):
        super().__init__()
        self.ds = ds

    def add_pipeline(self, name, pipeline):
        super().add_pipeline(name, pipeline)
        self.ds._add_pipeline(name, pipeline)

    def get_pipeline(self, name):
        try:
            p = self.ds._client.get_pipeline(self.ds.name, name)
            pipeline = Pipeline.load(p, self)
            self.add_pipeline(name, pipeline)
            return pipeline
        except:
            return super().get_pipeline(name)

    def remove_pipeline(self, name):
        super().remove_pipeline(name)
        self.ds._remove_pipeline(name)


class Dataset(CamelResource):

    """

    """

    def __init__(self, ds, client: DatasetsClient):
        super().__init__(ds, read_only=False)
        self._client = client
        self._work_dir = Path.cwd() / 'datasets' / self.name
        self._pipeline_loader = _DatasetPipelineLoader(self)
        if not self.pipelines:
            self.pipelines = {}

    @staticmethod
    def get_dataset(name, client: DatasetsClient):
        """
        Fetches a Dataset to work with.

        :param name: The name of the dataset to retrieve.
        :param client: The client instance to use.
        :return: A Dataset object.
        """
        uri = '/'.join(['datasets', name])
        log.debug('Getting dataset using URI: %s' % uri)
        r = client._serviceconnector.request('GET', uri)
        r.raise_for_status()

        return Dataset(r.json(), client)

    def get_dataframe(self):
        return self._client.get_dataframe(self.name)

    def get_stream(self):
        return self._client.get_stream(self.name)

    def as_pandas(self):
        df = self.get_dataframe()
        columns = df.get('columns')
        values = df.get('values')

        try:
            import pandas as pd
            return pd.DataFrame(values, columns=columns)
        except ImportError:
            log.warn('Pandas is not installed, please run `pip install pandas` or equivalent in your environment')
            return {'columns': columns, 'values': values}

    def data_dictionary(self, df=None):
        if df is None:
            df = self.as_pandas()
        return DataDiscovery.data_dictionary(df)

    def visuals(self, df=None, figsize=(18, 9)):
        if df is None:
            df = self.as_pandas()
        return _Viz(df, figsize)

    def contract(self, name):
        self._work_dir.mkdir(parents=True, exist_ok=True)

        tr = Transition(contract_name=name, working_path=str(self._work_dir))

        # Monkey patching
        patch_tr(tr)

        # Override get_source to redirect to the Dataset API
        tr.get_source = self.as_pandas
        tr.get_source_data = self.as_pandas

        return tr

    def save(self):
        from .builder.dataset_builder import DatasetBuilder
        b = DatasetBuilder(self.name, self._client, self.camel)
        return b.from_dataset(self).build()

    def to_camel(self):
        from .builder.dataset_builder import DatasetBuilder
        b = DatasetBuilder(self.name, self._client, self.camel)
        return b.to_camel()

    def _add_pipeline(self, name, pipeline):
        self.pipelines[name] = pipeline

    def _remove_pipeline(self, name):
        if name in self.pipelines:
            del self.pipelines[name]

    def pipeline(self, name, clear_cache=False, depends=None):
        p = self._pipeline_loader.get_pipeline(name)
        if clear_cache:
            # TODO clear any caches - e.g. for local mode
            pass

        if depends is not None:
            for d in depends:
                p.add_dependency(self._pipeline_loader.get_pipeline(d))

        return p
