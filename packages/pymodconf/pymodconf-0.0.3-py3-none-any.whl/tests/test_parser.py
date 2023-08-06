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

import unittest

from pymodconf.parser import load, InvalidConfigurationError
from pymodconf.tag import Tag, register
from tests import DEFAULT_TEST_FILE


class TestLoadModuleConfiguration(unittest.TestCase):

    def test_load_module_config_file(self):
        # register the test tag
        t = Tag('Module: ')
        register(t)

        # load the configuration
        config = load(DEFAULT_TEST_FILE)

        # check if tag is available
        self.assertIn(str(t), config)
        self.assertEqual(1, len(config[str(t)]))


class TestLoadDefaultConfiguration(unittest.TestCase):

    def test_load_default_config_file(self):
        # load the configuration
        load(DEFAULT_TEST_FILE)

    def test_hello(self):
        # load the configuration
        config = load(DEFAULT_TEST_FILE)

        self.assertIn('name', config)
        self.assertIn('string', config)
        self.assertEqual('Hello pymodconf!', config['string'])

        print(config['string'])

    def test_multiple_entries(self):
        # load the configuration
        config = load(DEFAULT_TEST_FILE)

        self.assertIn('list', config)
        self.assertEqual(4, len(config['list']))
        self.assertTrue(isinstance(config['list'], list))

    def test_multiple_entries_in_setion(self):
        # load the configuration
        config = load(DEFAULT_TEST_FILE)

        self.assertIn('Some Section', config)

        self.assertEqual('pymodconf-app-section', config['Some Section']['opt'])


class TestLoadConfigValidated(unittest.TestCase):

    def test_section_in_config(self):

        mapping = {
            'Some Section':
                ['opt']
        }

        try:
            self.config = load(DEFAULT_TEST_FILE, mapping)
        except InvalidConfigurationError:  # pragma: no cover
            self.fail('InvalidConfigurationError exception raised unexpectedly!')

    def test_section_missing_in_config(self):

        mapping = {
            'Some Section': [],
            'Another required section': []
        }

        with self.assertRaises(InvalidConfigurationError):
            self.config = load(DEFAULT_TEST_FILE, mapping)

    def test_option_missing_in_config(self):

        mapping = {
            'Some Section': ['required option']
        }

        with self.assertRaises(InvalidConfigurationError):
            self.config = load(DEFAULT_TEST_FILE, mapping)
