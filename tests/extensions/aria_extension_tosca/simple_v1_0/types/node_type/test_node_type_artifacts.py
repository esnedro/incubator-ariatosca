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


# TODO: properties


# Artifacts section

@pytest.mark.parametrize('value', data.NOT_A_DICT)
def test_node_type_artifacts_section_syntax_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    artifacts: {{ value }}
""", dict(value=value)).assert_failure()


def test_node_type_artifacts_section_syntax_empty(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    artifacts: {}
""").assert_success()


# Artifact

@pytest.mark.parametrize('value', data.NOT_A_DICT)
def test_node_type_artifact_syntax_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    artifacts:
      my_artifact: {{ value }}
""", dict(value=value)).assert_failure()


def test_node_type_artifact_syntax_unsupported(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
artifact_types:
  MyType: {}
node_types:
  MyType:
    artifacts:
      my_artifact:
        type: MyType
        file: a file
        unsupported: {}
""").assert_failure()


def test_node_type_artifact_syntax_empty(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    artifacts:
      my_artifact: {} # "type" and "file" are required
""").assert_failure()


# Type

@pytest.mark.parametrize('value', data.NOT_A_STRING)
def test_node_type_artifact_type_syntax_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    artifacts:
      my_artifact:
        type: {{ value }}
        file: a file
""", dict(value=value)).assert_failure()


def test_node_type_artifact_type_unknown(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    artifacts:
      my_artifact:
        type: UnknownType
        file: a file
""").assert_failure()


# File

@pytest.mark.parametrize('value', data.NOT_A_STRING)
def test_node_type_artifact_file_syntax_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
artifact_types:
  MyType: {}
node_types:
  MyType:
    artifacts:
      my_artifact:
        type: MyType
        file: {{ value }}
""", dict(value=value)).assert_failure()


def test_node_type_artifact_file(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
artifact_types:
  MyType: {}
node_types:
  MyType:
    artifacts:
      my_artifact:
        type: MyType
        file: a file
""").assert_success()


# Description

@pytest.mark.parametrize('value', data.NOT_A_STRING)
def test_node_type_artifact_description_syntax_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
artifact_types:
  MyType: {}
node_types:
  MyType:
    artifacts:
      my_artifact:
        type: MyType
        file: a file
        description: {{ value }}
""", dict(value=value)).assert_failure()


def test_node_type_artifact_description(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
artifact_types:
  MyType: {}
node_types:
  MyType:
    artifacts:
      my_artifact:
        type: MyType
        file: a file
        description: a description
""").assert_success()


# Repository

@pytest.mark.parametrize('value', data.NOT_A_STRING)
def test_node_type_artifact_repository_syntax_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
artifact_types:
  MyType: {}
node_types:
  MyType:
    artifacts:
      my_artifact:
        type: MyType
        file: a file
        repository: {{ value }}
""", dict(value=value)).assert_failure()


def test_node_type_artifact_repository_unknown(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
artifact_types:
  MyType: {}
node_types:
  MyType:
    artifacts:
      my_artifact:
        type: MyType
        file: a file
        repository: unknown
""").assert_failure()


def test_node_type_artifact_repository(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
repositories:
  my_repository:
    url: a url
artifact_types:
  MyType: {}
node_types:
  MyType:
    artifacts:
      my_artifact:
        type: MyType
        file: a file
        repository: my_repository
""").assert_success()


# Deploy path

@pytest.mark.parametrize('value', data.NOT_A_STRING)
def test_node_type_artifact_deploy_path_syntax_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
artifact_types:
  MyType: {}
node_types:
  MyType:
    artifacts:
      my_artifact:
        type: MyType
        file: a file
        deploy_path: {{ value }}
""", dict(value=value)).assert_failure()


def test_node_type_artifact_deploy_path(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
artifact_types:
  MyType: {}
node_types:
  MyType:
    artifacts:
      my_artifact:
        type: MyType
        file: a file
        deploy_path: a path
""").assert_success()


# Unicode

def test_node_type_artifact_unicode(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
repositories:
  知識庫:
    url: 網址
artifact_types:
  類型: {}
node_types:
  類型:
    artifacts:
      神器:
        type: 類型
        file: 文件
        repository: 知識庫
        deploy_path: 路徑
""").assert_success()
