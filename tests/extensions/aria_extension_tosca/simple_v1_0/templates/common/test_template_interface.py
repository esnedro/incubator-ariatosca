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

import itertools

import pytest

from ... import data


# Syntax

@pytest.mark.parametrize('name,value', itertools.product(
    data.TEMPLATE_WITH_INTERFACE_NAMES,
    data.NOT_A_DICT
))
def test_template_interfaces_wrong_yaml_type(parser, name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType: {}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces: {{ value }}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], value=value)).assert_failure()


@pytest.mark.parametrize('name', data.TEMPLATE_WITH_INTERFACE_NAMES)
def test_template_interfaces_empty(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType: {}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces: {}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name])).assert_success()


@pytest.mark.parametrize('name,value', itertools.product(
    data.TEMPLATE_WITH_INTERFACE_NAMES,
    data.NOT_A_DICT
))
def test_template_interface_wrong_yaml_type(parser, name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface: {{ value }}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], value=value)).assert_failure()


@pytest.mark.parametrize('name', data.TEMPLATE_WITH_INTERFACE_NAMES)
def test_template_interface_empty(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface: {}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name])).assert_success()


@pytest.mark.parametrize('name,value', itertools.product(
    data.TEMPLATE_WITH_INTERFACE_NAMES,
    data.NOT_A_DICT
))
def test_template_interface_inputs_wrong_yaml_type(parser, name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface:
          inputs: {{ value }}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], value=value)).assert_failure()


@pytest.mark.parametrize('name', data.TEMPLATE_WITH_INTERFACE_NAMES)
def test_template_interface_inputs_empty(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface:
          inputs: {}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name])).assert_success()


@pytest.mark.parametrize('name,value', itertools.product(
    data.TEMPLATE_WITH_INTERFACE_NAMES,
    data.NOT_A_DICT_OR_STRING
))
def test_template_interface_operation_wrong_yaml_type(parser, name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
        my_operation: {}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface:
          my_operation: {{ value }}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], value=value)).assert_failure()


@pytest.mark.parametrize('name', data.TEMPLATE_WITH_INTERFACE_NAMES)
def test_template_interface_operation_empty(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
        my_operation: {}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface:
          my_operation: {}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name])).assert_success()


@pytest.mark.parametrize('name,value', itertools.product(
    data.TEMPLATE_WITH_INTERFACE_NAMES,
    data.NOT_A_DICT_OR_STRING
))
def test_template_interface_operation_implementation_wrong_yaml_type(parser, name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
        my_operation: {}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface:
          my_operation:
            implementation: {{ value }}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], value=value)).assert_failure()


@pytest.mark.parametrize('name', data.TEMPLATE_WITH_INTERFACE_NAMES)
def test_template_interface_operation_implementation_unsupported_field(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
        my_operation: {}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface:
          my_operation:
            implementation:
              unsupported: {}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name])).assert_failure()


@pytest.mark.parametrize('name,value', itertools.product(
    data.TEMPLATE_WITH_INTERFACE_NAMES,
    data.NOT_A_STRING
))
def test_template_interface_operation_implementation_primary_wrong_yaml_type(parser, name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
        my_operation: {}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface:
          my_operation:
            implementation:
              primary: {{ value }}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], value=value)).assert_failure()


@pytest.mark.parametrize('name,value', itertools.product(
    data.TEMPLATE_WITH_INTERFACE_NAMES,
    data.NOT_A_STRING
))
def test_template_interface_operation_implementation_dependencies_wrong_yaml_type(parser, name,
                                                                                  value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
        my_operation: {}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface:
          my_operation:
            implementation:
              dependencies:
                - {{ value }}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], value=value)).assert_failure()


# Operations

@pytest.mark.parametrize('name', data.TEMPLATE_WITH_INTERFACE_NAMES)
def test_template_interface_operation_from_type(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
        my_operation: {}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface:
          my_operation: {}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name])).assert_success()


@pytest.mark.parametrize('name', data.TEMPLATE_WITH_INTERFACE_NAMES)
def test_template_interface_operation_from_interface_type(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType:
    my_operation: {}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface:
          my_operation: {}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name])).assert_success()


@pytest.mark.parametrize('name', data.TEMPLATE_WITH_INTERFACE_NAMES)
def test_template_interface_operation_missing(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface:
          my_operation: {}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name])).assert_failure()


# Interface inputs

@pytest.mark.parametrize(
    'name,type_name,value',
    ((s, v[0], v[1])
     for s, v in itertools.product(
         data.TEMPLATE_WITH_INTERFACE_NAMES,
         data.PARAMETER_VALUES))
)
def test_template_interface_input_from_type(parser, name, type_name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType:
    properties:
      my_field:
        type: string
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
        inputs:
          my_input:
            type: {{ type_name }}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface:
          inputs:
            my_input: {{ value }}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], type_name=type_name,
          value=value)).assert_success()


@pytest.mark.parametrize(
    'name,type_name,value',
    ((s, v[0], v[1])
     for s, v in itertools.product(
         data.TEMPLATE_WITH_INTERFACE_NAMES,
         data.PARAMETER_VALUES))
)
def test_template_interface_input_from_interface_type(parser, name, type_name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType:
    properties:
      my_field:
        type: string
interface_types:
  MyType:
    inputs:
      my_input:
        type: {{ type_name }}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface:
          inputs:
            my_input: {{ value }}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], type_name=type_name,
          value=value)).assert_success()


@pytest.mark.parametrize('name', data.TEMPLATE_WITH_INTERFACE_NAMES)
def test_template_interface_input_missing(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface:
          inputs:
            my_input: a value
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name])).assert_failure()


# Operation inputs

@pytest.mark.parametrize(
    'name,type_name,value',
    ((s, v[0], v[1])
     for s, v in itertools.product(
         data.TEMPLATE_WITH_INTERFACE_NAMES,
         data.PARAMETER_VALUES))
)
def test_template_interface_operation_input_from_type(parser, name, type_name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType:
    properties:
      my_field:
        type: string
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
        my_operation:
          inputs:
            my_input:
              type: {{ type_name }}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface:
          my_operation:
            inputs:
              my_input: {{ value }}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], type_name=type_name,
          value=value)).assert_success()


@pytest.mark.parametrize(
    'name,type_name,value',
    ((s, v[0], v[1])
     for s, v in itertools.product(
         data.TEMPLATE_WITH_INTERFACE_NAMES,
         data.PARAMETER_VALUES))
)
def test_template_interface_operation_input_from_interface_type(parser, name, type_name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType:
    properties:
      my_field:
        type: string
interface_types:
  MyType:
    my_operation:
      inputs:
        my_input:
          type: {{ type_name }}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface:
          my_operation:
            inputs:
              my_input: {{ value }}
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name], type_name=type_name,
          value=value)).assert_success()


@pytest.mark.skip(reason='fix')
@pytest.mark.parametrize('name', data.TEMPLATE_WITH_INTERFACE_NAMES)
def test_template_interface_operation_input_missing(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      MyInterface:
        type: MyType
        my_operation: {}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
      interfaces:
        MyInterface:
          my_operation:
            inputs:
              my_input: a value
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name])).assert_failure()


# Unicode

@pytest.mark.parametrize('name', data.TEMPLATE_WITH_INTERFACE_NAMES)
def test_template_interface_unicode(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  類型: {}
{{ name }}_types:
  類型:
    interfaces:
      接口:
        type: 類型
        手術:
          inputs:
            輸入:
              type: string
topology_template:
  {{ section }}:
    模板:
      type: 類型
      interfaces:
        接口:
          手術:
            inputs:
              輸入: 值
""", dict(name=name, section=data.TEMPLATE_NAME_SECTIONS[name])).assert_success()
