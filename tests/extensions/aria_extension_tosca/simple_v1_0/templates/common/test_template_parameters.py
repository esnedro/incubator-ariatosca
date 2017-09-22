# -*- coding: utf-8 -*-
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from ... import data
from ......mechanisms.utils import matrix


MAIN_MACROS = """
{% macro additions() %}
{%- endmacro %}
{% macro type_parameters() %}
    {{ parameter_section }}: {{ caller()|indent(6) }}
{%- endmacro %}
{% macro parameters() %}
      {{ parameter_section }}: {{ caller()|indent(8) }}
{%- endmacro %}
"""

INTERFACE_MACROS = """
{% macro additions() %}
{%- endmacro %}
{% macro type_parameters() %}
    interfaces:
      MyInterface:
        type: MyType
interface_types:
  MyType:
    {{ parameter_section }}: {{ caller()|indent(8) }}
{%- endmacro %}
{% macro parameters() %}
      interfaces:
        MyInterface:
          {{ parameter_section }}: {{ caller()|indent(12) }}
{%- endmacro %}
"""


OPERATION_MACROS = """
{% macro additions() %}
{%- endmacro %}
{% macro type_parameters() %}
    interfaces:
      MyInterface:
        type: MyType
interface_types:
  MyType:
    my_operation:
      {{ parameter_section }}: {{ caller()|indent(10) }}
{%- endmacro %}
{% macro parameters() %}
      interfaces:
        MyInterface:
          my_operation:
            {{ parameter_section }}: {{ caller()|indent(14) }}
{%- endmacro %}
"""

LOCAL_INTERFACE_MACROS = """
{% macro additions() %}
interface_types:
  MyType: {}
{%- endmacro %}
{% macro type_parameters() %}
    interfaces:
      MyInterface:
        type: MyType
        {{ parameter_section }}: {{ caller()|indent(10) }}
{%- endmacro %}
{% macro parameters() %}
      interfaces:
        MyInterface:
          {{ parameter_section }}: {{ caller()|indent(12) }}
{%- endmacro %}
"""

LOCAL_OPERATION_MACROS = """
{% macro additions() %}
interface_types:
  MyType: {}
{%- endmacro %}
{% macro type_parameters() %}
    interfaces:
      MyInterface:
        type: MyType
        my_operation:
          {{ parameter_section }}: {{ caller()|indent(12) }}
{%- endmacro %}
{% macro parameters() %}
      interfaces:
        MyInterface:
          my_operation:
            {{ parameter_section }}: {{ caller()|indent(14) }}
{%- endmacro %}
"""


RELATIONSHIP_TYPE_MACROS = """
{% macro additions() %}
capability_types:
  MyType: {}
interface_types:
  MyType: {}
{%- endmacro %}
{% macro type_parameters() %}
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
relationship_types:
  MyType:
    {{ parameter_section }}: {{ caller()|indent(6) }}
{%- endmacro %}
{% macro parameters() %}
      requirements:
        - my_requirement:
            relationship:
              {{ parameter_section }}: {{ caller()|indent(16) }}
{%- endmacro %}
"""


RELATIONSHIP_LOCAL_INTERFACE_MACROS = """
{% macro additions() %}
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType: {}
{%- endmacro %}
{% macro type_parameters() %}
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              MyInterface:
                type: MyType
                {{ parameter_section }}: {{ caller()|indent(18) }}
{%- endmacro %}
{% macro parameters() %}
      requirements:
        - my_requirement:
            relationship:
              interfaces:
                MyInterface:
                  {{ parameter_section }}: {{ caller()|indent(20) }}
{%- endmacro %}
"""

RELATIONSHIP_INTERFACE_MACROS = """
{% macro additions() %}
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
{%- endmacro %}
{% macro type_parameters() %}
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              MyInterface:
                type: MyType
interface_types:
  MyType:
    {{ parameter_section }}: {{ caller()|indent(8) }}
{%- endmacro %}
{% macro parameters() %}
      requirements:
        - my_requirement:
            relationship:
              interfaces:
                MyInterface:
                  {{ parameter_section }}: {{ caller()|indent(20) }}
{%- endmacro %}
"""

RELATIONSHIP_OPERATION_MACROS = """
{% macro additions() %}
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
{%- endmacro %}
{% macro type_parameters() %}
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              MyInterface:
                type: MyType
interface_types:
  MyType:
    my_operation:
      {{ parameter_section }}: {{ caller()|indent(10) }}
{%- endmacro %}
{% macro parameters() %}
      requirements:
        - my_requirement:
            relationship:
              interfaces:
                MyInterface:
                  my_operation:
                    {{ parameter_section }}: {{ caller()|indent(22) }}
{%- endmacro %}
"""


RELATIONSHIP_TYPE_INTERFACE_MACROS = """
{% macro additions() %}
capability_types:
  MyType: {}
interface_types:
  MyType: {}
{%- endmacro %}
{% macro type_parameters() %}
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
relationship_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
        {{ parameter_section }}: {{ caller()|indent(10) }}
{%- endmacro %}
{% macro parameters() %}
      requirements:
        - my_requirement:
            relationship:
              interfaces:
                MyInterface:
                  {{ parameter_section }}: {{ caller()|indent(20) }}
{%- endmacro %}
"""

RELATIONSHIP_TYPE_OPERATION_MACROS = """
{% macro additions() %}
capability_types:
  MyType: {}
interface_types:
  MyType: {}
{%- endmacro %}
{% macro type_parameters() %}
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
relationship_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
        my_operation:
          {{ parameter_section }}: {{ caller()|indent(12) }}
{%- endmacro %}
{% macro parameters() %}
      requirements:
        - my_requirement:
            relationship:
              interfaces:
                MyInterface:
                  my_operation:
                    {{ parameter_section }}: {{ caller()|indent(22) }}
{%- endmacro %}
"""


RELATIONSHIP_LOCAL_INTERFACE_MACROS = """
{% macro additions() %}
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType: {}
{%- endmacro %}
{% macro type_parameters() %}
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              MyInterface:
                type: MyType
                {{ parameter_section }}: {{ caller()|indent(18) }}
{%- endmacro %}
{% macro parameters() %}
      requirements:
        - my_requirement:
            relationship:
              interfaces:
                MyInterface:
                  {{ parameter_section }}: {{ caller()|indent(20) }}
{%- endmacro %}
"""

RELATIONSHIP_LOCAL_OPERATION_MACROS = """
{% macro additions() %}
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType: {}
{%- endmacro %}
{% macro type_parameters() %}
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              MyInterface:
                type: MyType
                my_operation:
                  {{ parameter_section }}: {{ caller()|indent(20) }}
{%- endmacro %}
{% macro parameters() %}
      requirements:
        - my_requirement:
            relationship:
              interfaces:
                MyInterface:
                  my_operation:
                    {{ parameter_section }}: {{ caller()|indent(22) }}
{%- endmacro %}
"""

MACROS = {
    'main': MAIN_MACROS,
    'interface': INTERFACE_MACROS,
    'operation': OPERATION_MACROS,
    'local-interface': LOCAL_INTERFACE_MACROS,
    'local-operation': LOCAL_OPERATION_MACROS,
    'relationship-type': RELATIONSHIP_TYPE_MACROS,
    'relationship-interface': RELATIONSHIP_INTERFACE_MACROS,
    'relationship-operation': RELATIONSHIP_OPERATION_MACROS,
    'relationship-type-interface': RELATIONSHIP_TYPE_INTERFACE_MACROS,
    'relationship-type-operation': RELATIONSHIP_TYPE_OPERATION_MACROS,
    'relationship-local-interface': RELATIONSHIP_LOCAL_INTERFACE_MACROS,
    'relationship-local-operation': RELATIONSHIP_LOCAL_OPERATION_MACROS
}

PARAMETER_SECTIONS = (
    ('main', 'node', 'properties'),
    ('main', 'node', 'attributes'),
    ('main', 'group', 'properties'),
    ('main', 'relationship', 'properties'),
    ('main', 'relationship', 'attributes'),
    ('main', 'policy', 'properties'),
    ('interface', 'node', 'inputs'),
    ('interface', 'group', 'inputs'),
    ('interface', 'relationship', 'inputs'),
    ('operation', 'node', 'inputs'),
    ('operation', 'group', 'inputs'),
    ('operation', 'relationship', 'inputs'),
    ('local-interface', 'node', 'inputs'),
    ('local-interface', 'group', 'inputs'),
    ('local-interface', 'relationship', 'inputs'),
    ('local-operation', 'node', 'inputs'),
    ('local-operation', 'group', 'inputs'),
    ('local-operation', 'relationship', 'inputs'),
    ('relationship-type', 'node', 'properties'),
    ('relationship-interface', 'node', 'inputs'),
    #('relationship-operation', 'node', 'inputs'), # fix
    ('relationship-type-interface', 'node', 'inputs'),
    ('relationship-type-operation', 'node', 'inputs'), # fix
    ('relationship-local-interface', 'node', 'inputs'),
    #('relationship-operation', 'node', 'inputs'), # fix
)

PROPERTY_SECTIONS = (
    ('main', 'node'),
    ('main', 'group'),
    ('main', 'relationship'),
    ('main', 'policy')
)


# Parameters section

@pytest.mark.parametrize('macros,name,parameter_section,value', matrix(
    PARAMETER_SECTIONS,
    data.NOT_A_DICT,
    counts=(3, 1)
))
def test_template_parameters_section_syntax_type(parser, macros, name, parameter_section, value):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call type_parameters() -%}
{}
{% endcall %}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
{%- call parameters() -%}
{{ value }}
{% endcall %}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          parameter_section=parameter_section, value=value)).assert_failure()


@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_template_parameters_section_syntax_empty(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call type_parameters() -%}
{}
{% endcall %}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
{%- call parameters() -%}
{}
{% endcall %}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          parameter_section=parameter_section)).assert_success()


# Parameter

@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_template_parameter_missing(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call type_parameters() -%}
{}
{% endcall %}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
{%- call parameters() %}
my_parameter: a value
{% endcall %}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          parameter_section=parameter_section)).assert_failure()


# Required (properties only)

@pytest.mark.parametrize('macros,name,type_name', matrix(
    PROPERTY_SECTIONS,
    data.PARAMETER_TYPE_NAMES,
    counts=(2, 1)
))
def test_template_property_required(parser, macros, name, type_name):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyType:
    properties:
      my_field:
        type: string
{{ name }}_types:
  MyType:
{%- call type_parameters() %}
my_property:
  type: {{ type_name }}
{% endcall %}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], parameter_section='properties',
          type_name=type_name)).assert_failure()


@pytest.mark.parametrize('macros,name,type_name', matrix(
    PROPERTY_SECTIONS,
    data.PARAMETER_TYPE_NAMES,
    counts=(2, 1)
))
def test_template_property_not_required(parser, macros, name, type_name):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyType:
    properties:
      my_field:
        type: string
{{ name }}_types:
  MyType:
{%- call type_parameters() %}
my_property:
  type: {{ type_name }}
  required: false
{% endcall %}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], parameter_section='properties',
          type_name=type_name)).assert_success()


@pytest.mark.parametrize('macros,name,type_name,value', matrix(
    PROPERTY_SECTIONS,
    data.PARAMETER_VALUES,
    counts=(2, 2)
))
def test_template_property_required_with_default(parser, macros, name, type_name, value):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyType:
    properties:
      my_field:
        type: string
{{ name }}_types:
  MyType:
{%- call type_parameters() %}
my_property:
  type: {{ type_name }}
  default: {{ value }}
{% endcall %}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], parameter_section='properties',
          type_name=type_name, value=value)).assert_success()


# Entry schema

@pytest.mark.parametrize('macros,name,parameter_section,values', matrix(
    PARAMETER_SECTIONS,
    data.ENTRY_SCHEMA_VALUES,
    counts=(3, 1)
))
def test_template_parameter_map(parser, macros, name, parameter_section, values):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyType:
    properties:
      my_field:
        type: string
        default: default value
{{ name }}_types:
  MyType:
{%- call type_parameters() %}
my_parameter:
  type: map
  entry_schema: {{ values[0] }}
{% endcall %}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
{%- call parameters() %}
my_parameter:
  key1: {{ values[1] }}
  key2: {{ values[2] }}
{% endcall %}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], parameter_section=parameter_section,
          values=values), import_profile=True).assert_success()


@pytest.mark.parametrize('macros,name,parameter_section,values', matrix(
    PARAMETER_SECTIONS,
    data.ENTRY_SCHEMA_VALUES_BAD,
    counts=(3, 1)
))
def test_template_parameter_map_bad(parser, macros, name, parameter_section, values):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyType:
    properties:
      my_field:
        type: string
        default: default value
{{ name }}_types:
  MyType:
{%- call type_parameters() %}
my_parameter:
  type: map
  entry_schema: {{ values[0] }}
{% endcall %}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
{%- call parameters() %}
my_parameter:
  key1: {{ values[1] }}
  key2: {{ values[2] }}
{% endcall %}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], parameter_section=parameter_section,
          values=values), import_profile=True).assert_failure()


@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_template_parameter_map_required_field(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyType:
    properties:
      my_field:
        type: string
{{ name }}_types:
  MyType:
{%- call type_parameters() %}
my_parameter:
  type: map
  entry_schema: MyType
{% endcall %}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
{%- call parameters() %}
my_parameter:
  key: {my_field: a value}
{% endcall %}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          parameter_section=parameter_section), import_profile=True).assert_success()


@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_template_parameter_map_required_field_bad(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyType:
    properties:
      my_field:
        type: string
{{ name }}_types:
  MyType:
{%- call type_parameters() %}
my_parameter:
  type: map
  entry_schema: MyType
{% endcall %}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
{%- call parameters() %}
my_parameter:
  key: {}
{% endcall %}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          parameter_section=parameter_section), import_profile=True).assert_failure()


@pytest.mark.parametrize('macros,name,parameter_section,values', matrix(
    PARAMETER_SECTIONS,
    data.ENTRY_SCHEMA_VALUES,
    counts=(3, 1)
))
def test_template_parameter_list(parser, macros, name, parameter_section, values):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyType:
    properties:
      my_field:
        type: string
        default: default value
{{ name }}_types:
  MyType:
{%- call type_parameters() %}
my_parameter:
  type: list
  entry_schema: {{ values[0] }}
{% endcall %}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
{%- call parameters() %}
my_parameter:
  - {{ values[1] }}
  - {{ values[2] }}
{% endcall %}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], parameter_section=parameter_section,
          values=values), import_profile=True).assert_success()


@pytest.mark.parametrize('macros,name,parameter_section,values', matrix(
    PARAMETER_SECTIONS,
    data.ENTRY_SCHEMA_VALUES_BAD,
    counts=(3, 1)
))
def test_template_parameter_list_bad(parser, macros, name, parameter_section, values):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyType:
    properties:
      my_field:
        type: string
        default: default value
{{ name }}_types:
  MyType:
{%- call type_parameters() %}
my_parameter:
  type: list
  entry_schema: {{ values[0] }}
{% endcall %}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
{%- call parameters() %}
my_parameter:
  - {{ values[1] }}
  - {{ values[2] }}
{% endcall %}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], parameter_section=parameter_section,
          values=values), import_profile=True).assert_failure()


@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_template_parameter_list_required_field(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyType:
    properties:
      my_field:
        type: string
{{ name }}_types:
  MyType:
{%- call type_parameters() %}
my_parameter:
  type: list
  entry_schema: MyType
{% endcall %}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
{%- call parameters() %}
my_parameter:
  - {my_field: a value}
{% endcall %}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          parameter_section=parameter_section), import_profile=True).assert_success()


@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_template_parameter_list_required_field_bad(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyType:
    properties:
      my_field:
        type: string
{{ name }}_types:
  MyType:
{%- call type_parameters() %}
my_parameter:
  type: list
  entry_schema: MyType
{% endcall %}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
{%- call parameters() %}
my_parameter:
  - {}
{% endcall %}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          parameter_section=parameter_section), import_profile=True).assert_failure()


# Unicode

@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_template_parameter_unicode(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  類型:
{%- call type_parameters() %}
參數:
  type: string
{% endcall %}
topology_template:
  {{ section }}:
    模板:
      type: 類型
{%- call parameters() %}
參數: 值
{% endcall %}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          parameter_section=parameter_section)).assert_success()
