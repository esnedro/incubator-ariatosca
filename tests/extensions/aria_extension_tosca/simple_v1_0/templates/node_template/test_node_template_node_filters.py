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
{% macro node_type() %}
    {}
{%- endmacro %}
{% macro node_filter() %}
      node_filter: {{ caller()|indent(8) }}
{%- endmacro %}
"""

REQUIREMENT_MACROS = """
{% macro node_type() %}
    capabilities:
      my_capability: MyType
    requirements:
      - my_requirement:
          capability: MyType
capability_types:
  MyType: {}
{%- endmacro %}
{% macro node_filter() %}
      requirements:
        - my_requirement:
            node: MyType
            node_filter: {{ caller()|indent(14) }}
{%- endmacro %}
"""

MACROS = {
    'main': MAIN_MACROS,
    'requirement': REQUIREMENT_MACROS
}

CASES = (
    'main', 'requirement'
)


@pytest.mark.parametrize('macros,value', matrix(CASES, data.NOT_A_DICT))
def test_node_template_node_filter_syntax_type(parser, macros, value):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType: {{- node_type() }}
topology_template:
  node_templates:
    my_node:
      type: MyType
{%- call node_filter() -%}
{{ value }}
{% endcall %}
""", dict(value=value)).assert_failure()


@pytest.mark.parametrize('macros', CASES)
def test_node_template_node_filter_syntax_unsupported(parser, macros):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType: {{- node_type() }}
topology_template:
  node_templates:
    my_node:
      type: MyType
{%- call node_filter() %}
unsupported: {}
{% endcall %}
""").assert_failure()


@pytest.mark.parametrize('macros', CASES)
def test_node_template_node_filter_syntax_empty(parser, macros):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType: {{- node_type() }}
topology_template:
  node_templates:
    my_node:
      type: MyType
{%- call node_filter() -%}
{}
{% endcall %}
""").assert_success()


# Properties section

@pytest.mark.parametrize('macros,value', matrix(CASES, data.NOT_A_LIST))
def test_node_template_node_filter_properties_section_syntax_type(parser, macros, value):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType: {{- node_type() }}
topology_template:
  node_templates:
    my_node:
      type: MyType
{%- call node_filter() %}
properties: {{ value }}
{% endcall %}
""", dict(value=value)).assert_failure()


@pytest.mark.parametrize('macros', CASES)
def test_node_template_node_filter_properties_section_syntax_empty(parser, macros):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType: {{- node_type() }}
topology_template:
  node_templates:
    my_node:
      type: MyType
{%- call node_filter() %}
properties: []
{% endcall %}
""").assert_success()


# Capabilities section

@pytest.mark.parametrize('macros,value', matrix(CASES, data.NOT_A_LIST))
def test_node_template_node_filter_capabilities_section_syntax_type(parser, macros, value):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType: {{- node_type() }}
topology_template:
  node_templates:
    my_node:
      type: MyType
{%- call node_filter() %}
capabilities: {{ value }}
{% endcall %}
""", dict(value=value)).assert_failure()


@pytest.mark.parametrize('macros', CASES)
def test_node_template_node_filter_capabilities_section_syntax_empty(parser, macros):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType: {{- node_type() }}
topology_template:
  node_templates:
    my_node:
      type: MyType
{%- call node_filter() %}
capabilities: []
{% endcall %}
""").assert_success()


# Capability

@pytest.mark.parametrize('macros,value', matrix(CASES, data.NOT_A_DICT))
def test_node_template_node_filter_capability_syntax_type(parser, macros, value):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType: {{- node_type() }}
topology_template:
  node_templates:
    my_node:
      type: MyType
{%- call node_filter() %}
capabilities:
  - my_capability: {{ value }}
{% endcall %}
""", dict(value=value)).assert_failure()


@pytest.mark.parametrize('macros', CASES)
def test_node_template_node_filter_capability_syntax_unsupported(parser, macros):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType: {{- node_type() }}
topology_template:
  node_templates:
    my_node:
      type: MyType
{%- call node_filter() %}
capabilities:
  - my_capability:
      unsupported: {}
{% endcall %}
""").assert_failure()


@pytest.mark.parametrize('macros', CASES)
def test_node_template_node_filter_capability_syntax_empty(parser, macros):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType: {{- node_type() }}
topology_template:
  node_templates:
    my_node:
      type: MyType
{%- call node_filter() %}
capabilities:
  - my_capability: {}
{% endcall %}
""").assert_success()


# Capability properties section

@pytest.mark.parametrize('macros,value', matrix(CASES, data.NOT_A_LIST))
def test_node_template_node_filter_capability_properties_section_syntax_type(parser, macros, value):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType: {{- node_type() }}
topology_template:
  node_templates:
    my_node:
      type: MyType
{%- call node_filter() %}
capabilities:
  - my_capability:
      properties: {{ value }}
{% endcall %}
""", dict(value=value)).assert_failure()


@pytest.mark.parametrize('macros', CASES)
def test_node_template_node_filter_capability_properties_section_syntax_empty(parser, macros):
    parser.parse_literal(MACROS[macros] + """
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType: {{- node_type() }}
topology_template:
  node_templates:
    my_node:
      type: MyType
{%- call node_filter() %}
capabilities:
  - my_capability:
      properties: []
{% endcall %}
""").assert_success()
