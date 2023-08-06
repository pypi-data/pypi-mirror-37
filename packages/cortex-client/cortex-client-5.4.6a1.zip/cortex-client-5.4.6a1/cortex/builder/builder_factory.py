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

from cortex_client import DatasetsClient, CatalogClient, ActionClient
from .dataset_builder import DatasetBuilder
from .skill_builder import SkillBuilder
from .action_builder import ActionBuilder
from .schema_builder import SchemaBuilder
from cortex.pipeline import Pipeline


class BuilderFactory:

    def __init__(self, client):
        self.client = client

    def dataset(self, name: str, camel_version='1.0.0') -> DatasetBuilder:
        ds_client = DatasetsClient(self.client._url, 3, self.client._token.token)
        return DatasetBuilder(name, ds_client, camel_version)

    def skill(self, name: str, camel_version='1.0.0') -> SkillBuilder:
        catalog_client = CatalogClient(self.client._url, 3, self.client._token.token)
        return SkillBuilder(name, catalog_client, camel_version)

    def action(self, name: str, camel_version='1.0.0'):
        action_client = ActionClient(self.client._url, 3, self.client._token.token)
        return ActionBuilder(name, action_client, camel_version)

    def schema(self, name: str, camel_version='1.0.0'):
        catalog_client = CatalogClient(self.client._url, 3, self.client._token.token)
        return SchemaBuilder(name, catalog_client, camel_version)

    def pipeline(self, name: str):
        return Pipeline(name)
