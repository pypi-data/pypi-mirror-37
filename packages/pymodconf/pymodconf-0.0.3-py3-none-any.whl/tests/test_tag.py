# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2018 by Lars Klitzke, Lars.Klitzke@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os
import unittest

from pymodconf import tag
from pymodconf.io import read
from pymodconf.parser import parse
from pymodconf.tag import Tag, register
from tests import DEFAULT_TEST_FILE


class TestTagCreation(unittest.TestCase):

    def test_create_tag(self):
        test_tag = Tag('TestTag: ')

        self.assertTrue('testtag' == str(test_tag))

    def test_register_tag(self):
        test_tag = Tag('TestTag: ')

        register(test_tag)

        from pymodconf.tag import _TAGS
        self.assertTrue(test_tag in _TAGS)

    def test_tag_available(self):
        test_tag = Tag('TestTag: ')

        register(test_tag)

        self.assertTrue(tag.available(test_tag))

    def test_tag_as_str_available(self):

        test_tag = Tag('TestTag: ')

        register(test_tag)

        self.assertTrue(tag.available('TestTag:'))


class ModuleInConfig(unittest.TestCase):

    def setUp(self):
        self.testtag = Tag('Module:')
        register(self.testtag)

    def test_load_config(self):

        parser = read(DEFAULT_TEST_FILE)

        config = parse(parser)

        self.assertTrue(str(self.testtag) in config)
        self.assertEqual(1, len(config[str(self.testtag)]))
        self.assertTrue(len(list(config.keys())), 1)

        # check if the module section is present
        self.assertIn('Test', [s['name'] for s in config[str(self.testtag)]])

        # check if the option is available, too.
        self.assertIn('log-dir', config[str(self.testtag)][0])
