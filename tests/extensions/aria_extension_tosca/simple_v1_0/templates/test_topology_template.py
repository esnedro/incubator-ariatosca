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

from .. import data


# Syntax

@pytest.mark.parametrize('value', data.NOT_A_DICT)
def test_topology_template_wrong_yaml_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
topology_template: {{ value }}
""", dict(value=value)).assert_failure()


def test_topology_template_unsupported_field(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
topology_template:
    unsupported: {}
""").assert_failure()


def test_topology_template_empty(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
topology_template: {}
""").assert_success()


@pytest.mark.parametrize('name,value', itertools.product(
    data.TEMPLATE_NAMES,
    data.NOT_A_DICT
))
def test_topology_template_template_section_wrong_yaml_type(parser, name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
topology_template:
  {{ section }}: {{ value }}
""", dict(section=data.TEMPLATE_NAME_SECTIONS[name], value=value)).assert_failure()


@pytest.mark.parametrize('name', data.TEMPLATE_NAMES)
def test_topology_template_template_section_empty(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
topology_template:
  {{ section }}: {}
""", dict(section=data.TEMPLATE_NAME_SECTIONS[name])).assert_success()


def test_topology_template_fields(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType: {}
topology_template:
  description: a description
  substitution_mappings:
    node_type: MyType
""").assert_success()


# Unicode

def test_topology_template_unicode(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  類型: {}
topology_template:
  description: 描述
  substitution_mappings:
    node_type: 類型
""").assert_success()
