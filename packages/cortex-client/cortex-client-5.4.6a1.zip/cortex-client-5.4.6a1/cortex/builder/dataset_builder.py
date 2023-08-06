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

import tempfile
import shutil
from cortex.utils import md5sum, log_message
from cortex.logger import getLogger
from cortex.dataset import Dataset
from cortex_client import DatasetsClient, ConnectionClient, CatalogClient


log = getLogger(__name__)


class DatasetBuilder:

    """
    A builder utility to aid in programmatic creation of Cortex Datasets.  Not meant to be directly instantiated by
    clients.
    """

    def __init__(self, name: str, client: DatasetsClient, camel='1.0.0'):
        self._camel = camel
        self._name = name
        self._title = ' '
        self._description = ' '
        self._client = client
        self._connections = {}
        self._parameters = []
        self._schema_name = None
        self._schema_title = None
        self._schema_description = None

    def title(self, title: str):
        """
        Sets the title property of the Dataset.
        :param title: the human friendly name of the Dataset
        :return: the builder instance
        """
        self._title = title
        return self

    def description(self, description: str):
        """
        Sets the description property of the Dataset.
        :param description: the human friendly long description of the Dataset
        :return: the builder instance
        """
        self._description = description
        return self

    def from_csv(self, file_name, **kwargs):
        try:
            import pandas as pd
            return self.from_df(pd.read_csv(file_name, **kwargs), format='csv')
        except ImportError:
            raise Exception('from_csv requires Pandas to be installed!')

    def from_json(self, file_name, **kwargs):
        try:
            import pandas as pd
            return self.from_df(pd.read_json(file_name, **kwargs), format='json')
        except ImportError:
            raise Exception('from_json requires Pandas to be installed!')

    def from_df(self, df, format='json'):
        """
        Sets the content of the dataset to the provided Pandas DataFrame.  The DataFrame will be serialized and
        uploaded to the Cortex Managed Content service in the specified path.

        :param df: the Pandas DataFrame to use
        :param format: One of 'json', or 'csv'.
        :return: the builder instance
        """

        # Reset connection and parameters
        self._connections = {}
        self._parameters = []

        content_client = client = ConnectionClient(
            self._client._serviceconnector.url,
            2,
            self._client._serviceconnector.token
        )

        content_query = [
            {'name': 'contentType', 'value': format.upper()}
        ]

        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
                temp_path = temp.name
                content_type = 'text/csv'
                if format.lower() == 'json':
                    content_type = 'application/json'
                    content_query.append({'name': 'json/style', 'value': 'lines'})

                    # Use the 'records' format and JSON lines style file
                    df.to_json(temp, orient='records', lines=True)
                elif format.lower() == 'csv':
                    content_query.append({'name': 'csv/delimiter', 'value': ','})
                    content_query.append({'name': 'csv/headerRow', 'value': True})

                    # Stick to Pandas defaults for CSV
                    df.to_csv(temp)
                else:
                    raise Exception('Invalid format %s, must be either "json" or "csv"' % format)

            md5 = md5sum(temp_path)
            upload_key = '/cortex/datasets/%s/%s.%s' % (self._name, md5, format.lower())
            content_query.append({'name': 'key', 'value': upload_key})

            if not content_client.exists(upload_key):
                log_message('file version not found, pushing to remote storage: ' + upload_key, log)
                with open(temp_path, 'rb') as f:
                    content_client.uploadStreaming(key=upload_key, content_type=content_type, stream=f)
        finally:
            shutil.rmtree(temp_path, ignore_errors=True)

        self._connections['default'] = {
            'name': 'cortex/content',
            'type': 'managedContent',
            'query': content_query
        }

        for c in df.columns.values:
            # assume 'string' type, look for boolean, numeric, date, object
            param_type = 'string'
            param_format = None

            dtype = df[c].dtype
            if dtype.name == 'bool':
                param_type = 'boolean'
            elif dtype.name == 'object':
                param_type = 'string'
            elif dtype.name.startswith('int'):
                param_type = 'integer'
                param_format = 'int64'
            elif dtype.name.startswith('float'):
                param_type = 'number'
                param_format = 'float'
            elif dtype.name.startswith('date'):
                param_type = 'integer'
                param_format = 'timestamp.epoch'

            if param_format:
                self._parameters.append({'name': c, 'type': param_type, 'format': param_format})
            else:
                self._parameters.append({'name': c, 'type': param_type})

        return self

    def create_schema(self, name: str, title: str = None, description: str = None):
        """
        Will create or update a new schema (type) based on the message parameters set in the builder once build is
        called. The Cortex Dataset will refer to this schema instead of embedding the parameters inline.

        :param name: the resource name of the new schema
        :param title: human friendly display name
        :param description: human friendly long description
        :return: the builder instance
        """
        self._schema_name = name
        self._schema_title = title
        self._schema_description = description
        return self

    def to_camel(self):
        ds = {
            'camel': self._camel,
            'name': self._name,
            'title': self._title,
            'description': self._description,
            'parameters': self._parameters
        }

        # Create/update a schema for the declared Dataset parameters
        if self._schema_name:
            catalog_client = CatalogClient(
                self._client._serviceconnector.url,
                3,
                self._client._serviceconnector.token
            )

            schema = {
                'camel': self._camel,
                'name': self._schema_name,
                'title': self._schema_title or '',
                'description': self._schema_description or '',
                'parameters': self._parameters
            }

            catalog_client.save_type(schema)
            ds['parameters'] = {'$ref': self._schema_name}

        if self._camel == '1.0.0':
            ds['connectionName'] = self._connections.get('default', {}).get('name')
            ds['connectionQuery'] = self._connections.get('default', {}).get('query')
        else:
            ds['connections'] = self._connections

        return ds

    def build(self) -> Dataset:
        """
        Builds and saves a Dataset using the properties configured on the builder
        :return: the resulting Dataset
        """
        ds = self.to_camel()

        # Save the newly built dataset
        self._client.save_dataset(ds)

        return Dataset.get_dataset(self._name, self._client)
