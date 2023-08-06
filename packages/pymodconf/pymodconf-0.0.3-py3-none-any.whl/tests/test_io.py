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
import tempfile
import unittest

from pymodconf import io
from tests import DEFAULT_TEST_FILE


class TestCreateDirectories(unittest.TestCase):

    def setUp(self):
        # use a temporary base directory for our tests
        self.test_dir = tempfile.TemporaryDirectory()

    def test_create_single_directory(self):
        test_dir = 'testit'

        config = {
            'A': {
                'test-dir': os.path.join(self.test_dir.name, test_dir)
            }
        }

        # create the directory
        io.mkdirs(config)

        # check if directory was created
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir.name, test_dir)))

    def test_create_multiple_directories(self):
        test_dir1 = 'testit1'
        test_dir2 = 'testit2'
        test_dir3 = 'testit3'

        config = {
            'A': {
                'test1-dir': os.path.join(self.test_dir.name, test_dir1),
                'test2-dir': os.path.join(self.test_dir.name, test_dir2),
                'test3-dir': os.path.join(self.test_dir.name, test_dir3),
            }
        }

        # create the directories
        io.mkdirs(config)

        # check if all directories were created
        for directory in config['A'].values():
            self.assertTrue(os.path.isdir(directory))

    def test_create_directory_tree(self):
        test_dir = os.path.join('A', 'B', 'C', 'D')

        config = {
            'A': {
                'test-dir': os.path.join(self.test_dir.name, test_dir)
            }
        }

        io.mkdirs(config)

        self.assertTrue(os.path.isdir(os.path.join(self.test_dir.name, test_dir)))

    def tearDown(self):
        self.test_dir.cleanup()


class TestReadConfiguration(unittest.TestCase):

    def test_read_module_configuration(self):

        parser = io.read(DEFAULT_TEST_FILE)

        self.assertIsNotNone(parser)

    def test_read_missing_configuration(self):

        with self.assertRaises(FileNotFoundError):
            io.read('/lsajdlad.cfg')
