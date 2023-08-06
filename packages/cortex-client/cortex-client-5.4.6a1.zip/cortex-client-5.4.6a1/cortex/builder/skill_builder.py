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

from cortex.skill import Skill
from cortex_client import CatalogClient
from cortex.action import Action


class InputBuilder:

    def __init__(self, name: str, parent, camel='1.0.0'):
        self._name = name
        self._title = None
        self._description = None
        self._parent = parent
        self._routing = None
        self._routing_config = {}
        self._parameters = {}
        self._is_schema_ref = False

    def title(self, title: str):
        """
        Sets the title property of the Skill Input.
        :param title: the human friendly name of the Skill Input
        :return: the builder instance
        """
        self._title = title
        return self

    def description(self, description: str):
        """
        Sets the description property of the Skill Input.
        :param description: the human friendly long description of the Skill Input
        :return: the builder instance
        """
        self._description = description
        return self

    def all_routing(self, action, output: str):
        self._routing = 'all'
        if isinstance(action, Action):
            self._routing_config['action'] = action.name
        else:
            self._routing_config['action'] = repr(action)

        self._routing_config['output'] = output

        return self

    def parameter(self, name: str, type: str, format: str=None, title=None, description=None, required=True):
        """
        Adds an Input Message parameter/field.

        :param name:
        :param type:
        :param format:
        :param title:
        :param description:
        :param required:
        :return:
        """
        if self._is_schema_ref:
            raise Exception('Schema ref already used, parameters not allowed')

        param = {'name': name, 'type': type, 'required': required}

        if title:
            param['title'] = title

        if description:
            param['description'] = description

        if format:
            param['format'] = format

        self._parameters[name] = param

        return self

    def use_schema(self, name):
        """
        Use a schema reference to define the Input Message parameters.

        :param name:
        :return:
        """
        self._parameters['$ref'] = {'$ref': name}
        self._is_schema_ref = True
        return self

    def build(self):
        routing = {self._routing: self._routing_config}

        params = list(self._parameters.values())
        if len(params) == 1:
            if '$ref' in params[0]:
                params = params[0]

        skill_input = {
            'name': self._name,
            'title': self._title or self._name,
            'parameters': params,
            'routing': routing
        }

        if self._description:
            skill_input['description'] = self._description

        self._parent._inputs[self._name] = skill_input

        return self._parent


class OutputBuilder:

    def __init__(self, name: str, parent, camel='1.0.0'):
        self._name = name
        self._title = None
        self._description = None
        self._parent = parent
        self._parameters = {}
        self._is_schema_ref = False

    def title(self, title: str):
        """
        Sets the title property of the Skill Output.
        :param title: the human friendly name of the Skill Output
        :return: the builder instance
        """
        self._title = title
        return self

    def description(self, description: str):
        """
        Sets the description property of the Skill Output.
        :param description: the human friendly long description of the Skill Output
        :return: the builder instance
        """
        self._description = description
        return self

    def parameter(self, name: str, type: str, format: str=None, title=None, description=None, required=True):
        """
        Adds an Output Message parameter/field.

        :param name:
        :param type:
        :param format:
        :param title:
        :param description:
        :param required:
        :return:
        """
        if self._is_schema_ref:
            raise Exception('Schema ref already used, parameters not allowed')

        self._parameters[name] = {'name': name, 'type': type, 'required': required}

        if title:
            self._parameters[name]['title'] = title

        if description:
            self._parameters[name]['description'] = description

        if format:
            self._parameters[name]['format'] = format

        return self

    def use_schema(self, name):
        """
        Use a schema reference to define the Output Message parameters.

        :param name:
        :return:
        """
        self._parameters['$ref'] = {'$ref': name}
        self._is_schema_ref = True
        return self

    def build(self):
        params = list(self._parameters.values())
        if len(params) == 1:
            if '$ref' in params[0]:
                params = params[0]

        skill_output = {
            'name': self._name,
            'title': self._title or self._name,
            'parameters': params
        }

        if self._description:
            skill_output['description'] = self._description

        self._parent._outputs[self._name] = skill_output

        return self._parent


class SkillBuilder:

    """
    A builder utility to aid in programmatic creation of Cortex Skills.  Not meant to be directly instantiated by
    clients.
    """

    def __init__(self, name: str, client: CatalogClient, camel='1.0.0'):
        self._camel = camel
        self._name = name
        self._title = None
        self._description = None
        self._client = client
        self._inputs = {}
        self._outputs = {}
        self._properties = {}

    def title(self, title: str):
        """
        Sets the title property of the Skill.
        :param title: the human friendly name of the Skill
        :return: the builder instance
        """
        self._title = title
        return self

    def description(self, description: str):
        """
        Sets the description property of the Skill.
        :param description: the human friendly long description of the Skill
        :return: the builder instance
        """
        self._description = description
        return self

    def property(self, name: str, data_type: str, title: str=None, description: str=None, required: bool=True, secure=False, default_val: str=None, valid_values=None):
        """
        Adds a Skill property.  Skill properties can be configured on a per instance basis and are passed down to Actions for use.

        :param name:
        :param data_type:
        :param title:
        :param description:
        :param required:
        :param secure:
        :param default_val:
        :param valid_values:
        :return:
        """
        prop ={
            'name': name,
            'type': data_type,
            'required': required,
            'secure': secure
        }

        if title:
            prop['title'] = title

        if description:
            prop['description'] = description

        if default_val:
            prop['defaultValue'] = default_val

        if valid_values:
            prop['validValues'] = valid_values

        self._properties[name] = prop

        return self

    def input(self, name: str):
        """
        Adds a Skill Input.
        :param name:
        :return:
        """
        return InputBuilder(name, self, self._camel)

    def output(self, name: str):
        """
        Adds a Skill Output.
        :param name:
        :return:
        """
        return OutputBuilder(name, self, self._camel)

    def to_camel(self):
        skill = {
            'camel': self._camel,
            'name': self._name,
            'title': self._title or self._name,
            'inputs': list(self._inputs.values()),
            'outputs': list(self._outputs.values())
        }

        if len(self._properties) > 0:
            skill['properties'] = list(self._properties.values())

        if self._description:
            skill['description'] = self._description

        return skill

    def build(self) -> Skill:
        """
        Builds and saves a Skill using the properties configured on the builder
        :return: the resulting Skill
        """
        skill = self.to_camel()
        self._client.save_skill(skill)

        return Skill.get_skill(self._name, self._client._serviceconnector)
