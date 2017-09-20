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


# Syntax

@pytest.mark.parametrize('name,parameter_section,value', matrix(
    data.TEMPLATE_PARAMETER_SECTIONS,
    data.NOT_A_DICT,
    counts=(2, 1)
))
def test_template_parameter_section_syntax_type(parser, name, parameter_section, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType: {}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      {{ parameter_section }}: {{ value }}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          parameter_section=parameter_section, value=value)).assert_failure()


@pytest.mark.parametrize('name,parameter_section', data.TEMPLATE_PARAMETER_SECTIONS)
def test_template_parameter_section_syntax_empty(parser, name, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType: {}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      {{ parameter_section }}: {}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          parameter_section=parameter_section)).assert_success()


@pytest.mark.parametrize('name,parameter_section', data.TEMPLATE_PARAMETER_SECTIONS)
def test_template_parameter_syntax_unsupported(parser, name, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType: {}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      {{ parameter_section }}:
        my_parameter:
          unsupported: {}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          parameter_section=parameter_section)).assert_failure()


# Type conformance

@pytest.mark.parametrize('name,parameter_section', data.TEMPLATE_PARAMETER_SECTIONS)
def test_template_parameter_missing(parser, name, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType:
    {{ parameter_section }}:
      my_parameter1:
        type: string
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      {{ parameter_section }}:
        my_parameter2: a value
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          parameter_section=parameter_section)).assert_failure()


@pytest.mark.parametrize('name,type_name', matrix(
    data.TEMPLATE_NAMES,
    data.PARAMETER_TYPE_NAMES
))
def test_template_property_required(parser, name, type_name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType:
    properties:
      my_field:
        type: string
{{ name }}_types:
  MyType:
    properties:
      my_property:
        type: {{ type_name }}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          type_name=type_name)).assert_failure()


@pytest.mark.parametrize('name,type_name', matrix(
    data.TEMPLATE_NAMES,
    data.PARAMETER_TYPE_NAMES
))
def test_template_property_not_required(parser, name, type_name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType:
    properties:
      my_field:
        type: string
{{ name }}_types:
  MyType:
    properties:
      my_property:
        type: {{ type_name }}
        required: false
topology_template:
  {{ section }}:
    my_template:
      type: MyType
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          type_name=type_name)).assert_success()


@pytest.mark.parametrize('name,type_name,value', matrix(
    data.TEMPLATE_NAMES,
    data.PARAMETER_VALUES,
    counts=(1, 2)
))
def test_template_property_required_with_default(parser, name, type_name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType:
    properties:
      my_field:
        type: string
{{ name }}_types:
  MyType:
    properties:
      my_property:
        type: {{ type_name }}
        default: {{ value }}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], type_name=type_name,
          value=value)).assert_success()


# Entry schema

@pytest.mark.parametrize('name,parameter_section,values', matrix(
    data.TEMPLATE_PARAMETER_SECTIONS,
    data.ENTRY_SCHEMA_VALUES,
    counts=(2, 1)
))
def test_template_parameter_map(parser, name, parameter_section, values):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType:
    properties:
      my_field:
        type: string
        default: default value
{{ name }}_types:
  MyType:
    {{ parameter_section }}:
      my_parameter:
        type: map
        entry_schema: {{ values[0] }}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      {{ parameter_section }}:
        my_parameter:
          key1: {{ values[1] }}
          key2: {{ values[2] }}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], parameter_section=parameter_section,
          values=values)).assert_success()


@pytest.mark.parametrize('name,parameter_section,values', matrix(
    data.TEMPLATE_PARAMETER_SECTIONS,
    data.ENTRY_SCHEMA_VALUES_BAD,
    counts=(2, 1)
))
def test_template_parameter_map_bad(parser, name, parameter_section, values):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType:
    properties:
      my_field:
        type: string
        default: default value
{{ name }}_types:
  MyType:
    {{ parameter_section }}:
      my_parameter:
        type: map
        entry_schema: {{ values[0] }}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      {{ parameter_section }}:
        my_parameter:
          key1: {{ values[1] }}
          key2: {{ values[2] }}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], parameter_section=parameter_section,
          values=values)).assert_failure()


@pytest.mark.parametrize('name,parameter_section', data.TEMPLATE_PARAMETER_SECTIONS)
def test_template_parameter_map_required_field(parser, name, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType:
    properties:
      my_field:
        type: string
{{ name }}_types:
  MyType:
    {{ parameter_section }}:
      my_parameter:
        type: map
        entry_schema: MyType
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      {{ parameter_section }}:
        my_parameter:
          key: {my_field: a value}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          parameter_section=parameter_section)).assert_success()


@pytest.mark.parametrize('name,parameter_section', data.TEMPLATE_PARAMETER_SECTIONS)
def test_template_parameter_map_required_field_bad(parser, name, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType:
    properties:
      my_field:
        type: string
{{ name }}_types:
  MyType:
    {{ parameter_section }}:
      my_parameter:
        type: map
        entry_schema: MyType
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      {{ parameter_section }}:
        my_parameter:
          key: {}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          parameter_section=parameter_section)).assert_failure()


@pytest.mark.parametrize('name,parameter_section,values', matrix(
    data.TEMPLATE_PARAMETER_SECTIONS,
    data.ENTRY_SCHEMA_VALUES,
    counts=(2, 1)
))
def test_template_parameter_list(parser, name, parameter_section, values):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType:
    properties:
      my_field:
        type: string
        default: default value
{{ name }}_types:
  MyType:
    {{ parameter_section }}:
      my_parameter:
        type: list
        entry_schema: {{ values[0] }}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      {{ parameter_section }}:
        my_parameter:
          - {{ values[1] }}
          - {{ values[2] }}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], parameter_section=parameter_section,
          values=values)).assert_success()


@pytest.mark.parametrize('name,parameter_section,values', matrix(
    data.TEMPLATE_PARAMETER_SECTIONS,
    data.ENTRY_SCHEMA_VALUES_BAD,
    counts=(2, 1)
))
def test_template_parameter_list_bad(parser, name, parameter_section, values):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType:
    properties:
      my_field:
        type: string
        default: default value
{{ name }}_types:
  MyType:
    {{ parameter_section }}:
      my_parameter:
        type: list
        entry_schema: {{ values[0] }}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      {{ parameter_section }}:
        my_parameter:
          - {{ values[1] }}
          - {{ values[2] }}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], parameter_section=parameter_section,
          values=values)).assert_failure()


@pytest.mark.parametrize('name,parameter_section', data.TEMPLATE_PARAMETER_SECTIONS)
def test_template_parameter_list_required_field(parser, name, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType:
    properties:
      my_field:
        type: string
{{ name }}_types:
  MyType:
    {{ parameter_section }}:
      my_parameter:
        type: list
        entry_schema: MyType
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      {{ parameter_section }}:
        my_parameter:
          - {my_field: a value}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          parameter_section=parameter_section)).assert_success()


@pytest.mark.parametrize('name,parameter_section', data.TEMPLATE_PARAMETER_SECTIONS)
def test_template_parameter_list_required_field_bad(parser, name, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType:
    properties:
      my_field:
        type: string
{{ name }}_types:
  MyType:
    {{ parameter_section }}:
      my_parameter:
        type: list
        entry_schema: MyType
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      {{ parameter_section }}:
        my_parameter:
          - {}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          parameter_section=parameter_section)).assert_failure()


# Unicode

@pytest.mark.parametrize('name,parameter_section', data.TEMPLATE_PARAMETER_SECTIONS)
def test_template_parameter_unicode(parser, name, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  類型:
    {{ parameter_section }}:
      參數:
        type: string
topology_template:
  {{ section }}:
    模板:
      type: 類型
      {{ parameter_section }}:
        參數: 值
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name],
          parameter_section=parameter_section)).assert_success()
