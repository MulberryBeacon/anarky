#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Tests for the common user interface operations.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# --------------------------------------------------------------------------------------------------
import interface
import tempfile
import unittest


# Test class
# --------------------------------------------------------------------------------------------------
class InterfaceTests(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile()
        self.temp_directory = tempfile.TemporaryDirectory()

    def test_file_exists_none(self):
        with self.assertRaises(TypeError):
            interface.file_exists(None)

    def test_file_exists_empty(self):
        result = interface.file_exists(self.temp_file)
        self.assertEqual(result, True)

    def test_directory_exists_none(self):
        with self.assertRaises(TypeError):
            interface.directory_exists(None)

    def test_directory_exists_empty(self):
        result = interface.directory_exists(self.temp_directory)
        self.assertEqual(result, True)

    def tearDown(self):
        self.temp_file.close()
        self.temp_directory.close()


# Methods :: Execution and boilerplate
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

