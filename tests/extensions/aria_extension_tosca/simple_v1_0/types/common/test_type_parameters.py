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
{% macro parameters() %}
    {{ parameter_section }}: {{ caller()|indent(6) }}
{%- endmacro %}
"""

NESTED_MACROS = """
{% macro additions() %}
{%- endmacro %}
{% macro parameters() %}
    nested:
      {{ parameter_section }}: {{ caller()|indent(8) }}
{%- endmacro %}
"""

INTERFACE_MACROS = """
{% macro additions() %}
interface_types:
  MyType: {}
{%- endmacro %}
{% macro parameters() %}
    interfaces:
      my_interface:
        type: MyType
        {{ parameter_section }}: {{ caller()|indent(10) }}
{%- endmacro %}
"""

OPERATION_MACROS = """
{% macro additions() %}
interface_types:
  MyType: {}
{%- endmacro %}
{% macro parameters() %}
    interfaces:
      my_interface:
        type: MyType
        my_operation:
          {{ parameter_section }}: {{ caller()|indent(12) }}
{%- endmacro %}
"""

RELATIONSHIP_INTERFACE_MACROS = """
{% macro additions() %}
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType: {}
{%- endmacro %}
{% macro parameters() %}
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType
                {{ parameter_section }}: {{ caller()|indent(20) }}
{%- endmacro %}
"""

RELATIONSHIP_OPERATION_MACROS = """
{% macro additions() %}
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType: {}
{%- endmacro %}
{% macro parameters() %}
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType
                my_operation:
                  {{ parameter_section }}: {{ caller()|indent(22) }}
{%- endmacro %}
"""

CAPABILITY_MACROS = """
{% macro additions() %}
capability_types:
  MyType: {}
{%- endmacro %}
{% macro parameters() %}
    capabilities:
      my_capability:
        type: MyType
        {{ parameter_section }}: {{ caller()|indent(10) }}
{%- endmacro %}
"""

MACROS = {
    'main': MAIN_MACROS,
    'nested': NESTED_MACROS,
    'interface': INTERFACE_MACROS,
    'operation': OPERATION_MACROS,
    'relationship-interface': RELATIONSHIP_INTERFACE_MACROS,
    'relationship-operation': RELATIONSHIP_OPERATION_MACROS,
    'capability': CAPABILITY_MACROS
}

PARAMETER_SECTIONS = (
    ('main', 'node', 'properties'),
    ('main', 'node', 'attributes'),
    ('main', 'group', 'properties'),
    ('main', 'relationship', 'properties'),
    ('main', 'relationship', 'attributes'),
    ('main', 'capability', 'properties'),
    ('main', 'capability', 'attributes'),
    ('main', 'policy', 'properties'),
    ('main', 'interface', 'inputs'),
    ('main', 'artifact', 'properties'),
    ('main', 'data', 'properties'),
    ('nested', 'interface', 'inputs'),
    ('interface', 'node', 'inputs'),
    ('interface', 'group', 'inputs'),
    ('interface', 'relationship', 'inputs'),
    ('operation', 'node', 'inputs'),
    ('operation', 'group', 'inputs'),
    ('operation', 'relationship', 'inputs'),
    ('relationship-interface', 'node', 'inputs'),
    ('relationship-operation', 'node', 'inputs'),
    ('capability', 'node', 'properties'),
    ('capability', 'node', 'attributes')
)

PROPERTY_SECTIONS = (
    ('main', 'node', 'properties'),
    ('main', 'group', 'properties'),
    ('main', 'relationship', 'properties'),
    ('main', 'capability', 'properties'),
    ('main', 'policy', 'properties'),
    ('main', 'interface', 'inputs'),
    ('main', 'artifact', 'properties'),
    ('main', 'data', 'properties'),
    ('nested', 'interface', 'inputs'),
    ('interface', 'node', 'inputs'),
    ('interface', 'group', 'inputs'),
    ('interface', 'relationship', 'inputs'),
    ('operation', 'node', 'inputs'),
    ('operation', 'group', 'inputs'),
    ('operation', 'relationship', 'inputs'),
    ('relationship-interface', 'node', 'inputs'),
    ('relationship-operation', 'node', 'inputs'),
    ('capability', 'node', 'properties')
)


# Parameters section

@pytest.mark.parametrize('macros,name,parameter_section,value', matrix(
    PARAMETER_SECTIONS,
    data.NOT_A_DICT,
    counts=(3, 1)
))
def test_type_parameters_section_syntax_type(parser, macros, name, parameter_section, value):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() -%}
{{ value }}
{% endcall %}
""", dict(name=name, parameter_section=parameter_section, value=value)).assert_failure()


@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_type_parameters_section_syntax_empty(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() -%}
{}
{% endcall %}
""", dict(name=name, parameter_section=parameter_section)).assert_success()


# Parameter

@pytest.mark.parametrize('macros,name,parameter_section,value', matrix(
    PARAMETER_SECTIONS,
    data.NOT_A_DICT,
    counts=(3, 1)
))
def test_type_parameter_syntax_type(parser, macros, name, parameter_section, value):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
my_parameter: {{ value }}
{% endcall %}
""", dict(name=name, parameter_section=parameter_section, value=value)).assert_failure()


@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_type_parameter_syntax_empty(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
my_parameter: {} # type is required
{% endcall %}
""", dict(name=name, parameter_section=parameter_section)).assert_failure()


@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_type_parameter_syntax_unsupported(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
my_parameter:
  type: string
  unsupported: {}
{% endcall %}
""", dict(name=name, parameter_section=parameter_section)).assert_failure()


# Description

@pytest.mark.parametrize('macros,name,parameter_section,value', matrix(
    PARAMETER_SECTIONS,
    data.NOT_A_STRING,
    counts=(3, 1)
))
def test_type_parameter_description_syntax_type(parser, macros, name, parameter_section, value):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
my_parameter:
  type: string
  description: {{ value }}
{% endcall %}
""", dict(name=name, parameter_section=parameter_section, value=value)).assert_failure()


@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_type_parameter_description(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
my_parameter:
  type: string
  description: a description
{% endcall %}
""", dict(name=name, parameter_section=parameter_section)).assert_success()


# Default

@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_type_parameter_default(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
my_parameter:
  type: string
  default: a string
{% endcall %}
""", dict(name=name, parameter_section=parameter_section)).assert_success()


@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_type_parameter_default_bad(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
my_parameter:
  type: integer
  default: a string
{% endcall %}
""", dict(name=name, parameter_section=parameter_section)).assert_failure()


# Required

@pytest.mark.parametrize('macros,name,parameter_section,value', matrix(
    PARAMETER_SECTIONS,
    data.NOT_A_BOOL,
    counts=(3, 1)
))
def test_type_parameter_required_syntax_type(parser, macros, name, parameter_section, value):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
my_parameter:
  type: string
  required: {{ value }}
{% endcall %}
""", dict(name=name, parameter_section=parameter_section, value=value)).assert_failure()

@pytest.mark.parametrize('macros,name,parameter_section', PROPERTY_SECTIONS)
def test_type_parameter_required(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
my_parameter:
  type: string
  required: true
{% endcall %}
""", dict(name=name, parameter_section=parameter_section)).assert_success()


# Status

@pytest.mark.parametrize('macros,name,parameter_section,value', matrix(
    PARAMETER_SECTIONS,
    data.STATUSES,
    counts=(3, 1)
))
def test_type_parameter_status(parser, macros, name, parameter_section, value):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
my_parameter:
  type: string
  status: {{ value }}
{% endcall %}
""", dict(name=name, parameter_section=parameter_section, value=value)).assert_success()


@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_type_parameter_status_bad(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
my_parameter:
  type: string
  status: not a status
{% endcall %}
""", dict(name=name, parameter_section=parameter_section)).assert_failure()


# Constraints

@pytest.mark.parametrize('macros,name,parameter_section,value', matrix(
    PARAMETER_SECTIONS,
    data.NOT_A_LIST,
    counts=(3, 1)
))
def test_type_parameter_constraints_syntax_type(parser, macros, name, parameter_section, value):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
my_parameter:
  type: string
  constraints: {{ value }}
{% endcall %}
""", dict(name=name, parameter_section=parameter_section, value=value)).assert_failure()


@pytest.mark.parametrize('macros,name,parameter_section', PROPERTY_SECTIONS)
def test_type_parameter_constraints_syntax_empty(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
my_parameter:
  type: string
  constraints: []
{% endcall %}
""", dict(name=name, parameter_section=parameter_section)).assert_success()


@pytest.mark.parametrize('macros,name,parameter_section,constraint', matrix(
    PROPERTY_SECTIONS,
    data.CONSTRAINTS_WITH_VALUE,
    counts=(3, 1)
))
def test_type_parameter_constraints_with_value(parser, macros, name, parameter_section,
                                               constraint):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyDataType:
    properties:
      my_field:
        type: string
{%- if name != 'data' %}
{{ name }}_types:
{%- endif %}
  MyType:
{%- call parameters() %}
my_parameter:
  type: MyDataType
  constraints:
    - {{ constraint }}: {my_field: a string}
{% endcall %}
""", dict(name=name, parameter_section=parameter_section, constraint=constraint)).assert_success()


@pytest.mark.parametrize('macros,name,parameter_section,constraint', matrix(
    PROPERTY_SECTIONS,
    data.CONSTRAINTS_WITH_VALUE_LIST,
    counts=(3, 1)
))
def test_type_parameter_constraints_with_value_list(parser, macros, name, parameter_section,
                                                    constraint):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyDataType:
    properties:
      my_field:
        type: string
{%- if name != 'data' %}
{{ name }}_types:
{%- endif %}
  MyType:
{%- call parameters() %}
my_parameter:
  type: MyDataType
  constraints:
    - {{ constraint }}:
      - {my_field: string one}
      - {my_field: string two}
      - {my_field: string three}
{% endcall %}
""", dict(name=name, parameter_section=parameter_section, constraint=constraint)).assert_success()


@pytest.mark.parametrize('macros,name,parameter_section,constraint', matrix(
    PROPERTY_SECTIONS,
    data.CONSTRAINTS_WITH_VALUE_RANGE,
    counts=(3, 1)
))
def test_type_parameter_constraints_with_value_range(parser, macros, name, parameter_section,
                                                     constraint):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyDataType:
    properties:
      my_field:
        type: string
{%- if name != 'data' %}
{{ name }}_types:
{%- endif %}
  MyType:
{%- call parameters() %}
my_parameter:
  type: MyDataType
  constraints:
    - {{ constraint }}:
      - {my_field: string a}
      - {my_field: string b}
{% endcall %}
""", dict(name=name, parameter_section=parameter_section, constraint=constraint)).assert_success()


@pytest.mark.parametrize('macros,name,parameter_section,constraint', matrix(
    PROPERTY_SECTIONS,
    data.CONSTRAINTS_WITH_VALUE_RANGE,
    counts=(3, 1)
))
def test_type_parameter_constraints_with_value_range_too_many(parser, macros, name,
                                                              parameter_section, constraint):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyDataType:
    properties:
      my_field:
        type: string
{%- if name != 'data' %}
{{ name }}_types:
{%- endif %}
  MyType:
{%- call parameters() %}
my_parameter:
  type: MyDataType
  constraints:
    - {{ constraint }}:
      - {my_field: string a}
      - {my_field: string b}
      - {my_field: string c}
{% endcall %}
""", dict(name=name, parameter_section=parameter_section, constraint=constraint)).assert_failure()


@pytest.mark.parametrize('macros,name,parameter_section,constraint', matrix(
    PROPERTY_SECTIONS,
    data.CONSTRAINTS_WITH_VALUE_RANGE,
    counts=(3, 1)
))
def test_type_parameter_constraints_with_value_range_invalid(macros, parser, name,
                                                             parameter_section, constraint):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyDataType:
    properties:
      my_field:
        type: string
{%- if name != 'data' %}
{{ name }}_types:
{%- endif %}
  MyType:
{%- call parameters() %}
my_parameter:
  type: MyDataType
  constraints:
    - {{ constraint }}:
      - {my_field: string b}
      - {my_field: string a}
{% endcall %}
""", dict(name=name, parameter_section=parameter_section, constraint=constraint)).assert_failure()


@pytest.mark.parametrize('macros,name,parameter_section', PROPERTY_SECTIONS)
def test_type_parameter_constraints_pattern(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
my_parameter:
  type: string
  constraints:
    - pattern: ^pattern$
{% endcall %}
""", dict(name=name, parameter_section=parameter_section)).assert_success()


@pytest.mark.parametrize('macros,name,parameter_section', PROPERTY_SECTIONS)
def test_type_parameter_constraints_pattern_bad(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
my_parameter:
  type: string
  constraints:
    - pattern: (
{% endcall %}
""", dict(name=name, parameter_section=parameter_section)).assert_failure()


@pytest.mark.parametrize('macros,name,parameter_section,constraint', matrix(
    PROPERTY_SECTIONS,
    data.CONSTRAINTS_WITH_NON_NEGATIVE_INT,
    counts=(3, 1)
))
def test_type_parameter_constraints_with_integer(parser, macros, name, parameter_section,
                                                 constraint):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
my_parameter:
  type: string
  constraints:
    - {{ constraint }}: 1
{% endcall %}
""", dict(name=name, parameter_section=parameter_section, constraint=constraint)).assert_success()


@pytest.mark.parametrize('macros,name,parameter_section,constraint', matrix(
    PROPERTY_SECTIONS,
    data.CONSTRAINTS_WITH_NON_NEGATIVE_INT,
    counts=(3, 1)
))
def test_type_parameter_constraints_with_integer_bad(parser, macros, name, parameter_section,
                                                     constraint):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
my_parameter:
  type: string
  constraints:
    - {{ constraint }}: -1
{% endcall %}
""", dict(name=name, parameter_section=parameter_section, constraint=constraint)).assert_failure()


# Overriding

@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_type_parameter_add(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType1:
{%- call parameters() %}
my_parameter1:
  type: string
{% endcall %}
  MyType2:
    derived_from: MyType1
{%- call parameters() %}
my_parameter2:
  type: string
{% endcall %}
""", dict(name=name, parameter_section=parameter_section)).assert_success()


@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_type_parameter_add_default(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType1:
{%- call parameters() %}
my_parameter:
  type: string
{% endcall %}
  MyType2:
    derived_from: MyType1
{%- call parameters() %}
my_parameter:
  type: string
  default: my value
{% endcall %}
""", dict(name=name, parameter_section=parameter_section)).assert_success()


@pytest.mark.skip(reason='fix for node.capability and node.relationship')
@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_type_parameter_type_override(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyDataType1: {}
  MyDataType2:
    derived_from: MyDataType1
{%- if name != 'data' %}
{{ name }}_types:
{%- endif %}
  MyType1:
{%- call parameters() %}
my_parameter:
  type: MyDataType1
{% endcall %}
  MyType2:
    derived_from: MyType1
{%- call parameters() %}
my_parameter:
  type: MyDataType2
{% endcall %}
""", dict(name=name, parameter_section=parameter_section)).assert_success()


@pytest.mark.skip(reason='fix for node.capability and node.relationship')
@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_type_parameter_type_override_bad(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
data_types:
  MyDataType1: {}
  MyDataType2:
    derived_from: MyDataType1
{%- if name != 'data' %}
{{ name }}_types:
{%- endif %}
  MyType1:
{%- call parameters() %}
my_parameter:
  type: MyDataType2
{% endcall %}
  MyType2:
    derived_from: MyType1
{%- call parameters() %}
my_parameter:
  type: MyDataType1
{% endcall %}
""", dict(name=name, parameter_section=parameter_section)).assert_failure()


# Unicode

@pytest.mark.parametrize('macros,name,parameter_section', PARAMETER_SECTIONS)
def test_type_parameter_unicode(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  MyType:
{%- call parameters() %}
參數:
  type: string
  description: 描述
  default: 值
  status: supported
{% endcall %}
""", dict(name=name, parameter_section=parameter_section)).assert_success()


@pytest.mark.parametrize('macros,name,parameter_section', PROPERTY_SECTIONS)
def test_type_parameter_constraints_pattern_unicode(parser, macros, name, parameter_section):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
{{- additions() }}
{{ name }}_types:
  類型:
{%- call parameters() %}
參數:
  type: string
  constraints:
    - pattern: ^模式$
{% endcall %}
""", dict(name=name, parameter_section=parameter_section)).assert_success()
