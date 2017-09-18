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


# Keywords

TYPE_NAMES_NO_UNSUPPORTED_FIELDS = ('artifact', 'data', 'capability', 'relationship', 'node',
                                    'group', 'policy')
TYPE_NAMES = TYPE_NAMES_NO_UNSUPPORTED_FIELDS + ('interface',)
TYPE_NAME_PLURAL = {
    'artifact': 'artifacts',
    'data': 'datatypes',
    'capability': 'capabilities',
    'interface': 'interfaces',
    'relationship': 'relationships',
    'node': 'nodes',
    'group': 'groups',
    'policy': 'policies'
}
PRIMITIVE_TYPE_NAMES = ('string', 'integer', 'float', 'boolean')
PARAMETER_SECTION_NAMES = ('properties', 'attributes')
TEMPLATE_NAMES = ('node', 'group', 'relationship', 'policy')
TEMPLATE_WITH_INTERFACE_NAMES = ('node', 'group', 'relationship')
TEMPLATE_NAME_SECTIONS = {
    'node': 'node_templates',
    'group': 'groups',
    'relationship': 'relationship_templates',
    'policy': 'policies'
}
TEMPLATE_PARAMETER_SECTIONS = (
    ('node', 'properties'),
    ('node', 'attributes'),
    ('group', 'properties'),
    ('relationship', 'properties'),
    ('relationship', 'attributes'),
    ('policy', 'properties')
)
PARAMETER_SECTIONS = (
    ('artifact', 'properties'),
    ('data', 'properties'),
    ('capability', 'properties'),
    ('capability', 'attributes'),
    ('interface', 'inputs'),
    ('relationship', 'properties'),
    ('relationship', 'attributes'),
    ('node', 'properties'),
    ('node', 'attributes'),
    ('group', 'properties'),
    ('policy', 'properties')
)
PARAMETER_WITH_CONSTRAINTS_SECTIONS = (
    ('artifact', 'properties'),
    ('data', 'properties'),
    ('capability', 'properties'),
    ('interface', 'inputs'),
    ('relationship', 'properties'),
    ('node', 'properties'),
    ('group', 'properties'),
    ('policy', 'properties')
)
CONSTRAINTS_WITH_VALUE = ('equal', 'greater_than', 'greater_or_equal', 'less_than', 'less_or_equal')
CONSTRAINTS_WITH_VALUE_LIST = ('valid_values',)
CONSTRAINTS_WITH_VALUE_RANGE = ('in_range',)
CONSTRAINTS_WITH_NON_NEGATIVE_INT = ('length', 'min_length', 'max_length')

# Values

NOT_A_DICT = ('null', 'a string', '123', '0.123', '[]')
NOT_A_DICT_OR_STRING = ('null', '123', '0.123', '[]')
NOT_A_LIST = ('null', 'a string', '123', '0.123', '{}')
NOT_A_STRING = ('null', '123', '0.123', '[]', '{}')
NOT_A_RANGE = NOT_A_LIST + (
    '[]', '[ 1 ]', '[ 1, 2, 3 ]',
    '[ 1, 1 ]', '[ 2, 1 ]',
    '[ 1, a string ]', '[ a string, 1 ]',
    '[ 1.5, 2 ]', '[ 1, 2.5 ]'
)
NOT_OCCURRENCES = NOT_A_RANGE + ('[ -1, 1 ]',)
GOOD_VERSIONS = ("'6.1'", '2.0.1', '3.1.0.beta', "'1.0.0.alpha-10'")
BAD_VERSIONS = ('a_string', '1.2.3.4.5', '1.2.beta', '1.0.0.alpha-x')
STATUSES = ('supported', 'unsupported', 'experimental', 'deprecated')
PARAMETER_TYPE_NAMES = PRIMITIVE_TYPE_NAMES + ('MyType',)
PARAMETER_VALUES = (
    ('string', 'a string'),
    ('integer', '1'),
    ('float', '1.1'),
    ('MyType', '{my_field: a string}')
)
ENTRY_SCHEMA_VALUES = (
    ('string', 'a string', 'another string'),
    ('integer', '1', '2'),
    ('float', '1.1', '2.2'),
    ('MyType', '{my_field: a string}', '{}')
)
ENTRY_SCHEMA_VALUES_BAD = (
    ('string', 'a string', '1'),
    ('integer', '1', 'a string'),
    ('float', '1.1', 'a string'),
    ('MyType', '{my_field1: a string}', 'a string')
)
