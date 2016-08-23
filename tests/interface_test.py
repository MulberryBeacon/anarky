#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Tests for the common user interface operations.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# --------------------------------------------------------------------------------------------------
import library.interface as interface
import tempfile
import unittest


# Test class
# --------------------------------------------------------------------------------------------------
class InterfaceTests(unittest.TestCase):

    # Tests for method "file_exists"
    def test_file_exists_none(self):
        result = interface.file_exists(None)
        self.assertEqual(result, False)

    def test_file_exists_empty(self):
        result = interface.file_exists('')
        self.assertEqual(result, False)

    def test_file_exists(self):
        temp_file = tempfile.mkstemp()[1]
        result = interface.file_exists(temp_file)
        self.assertEqual(result, True)

    # Tests for method "directory_exists"
    def test_directory_exists_none(self):
        result = interface.directory_exists(None)
        self.assertEqual(result, False)

    def test_directory_exists_empty(self):
        result = interface.directory_exists('')
        self.assertEqual(result, False)

    def test_directory_exists(self):
        temp_directory = tempfile.mkdtemp()
        result = interface.directory_exists(temp_directory)
        self.assertEqual(result, True)


# Methods :: Execution and boilerplate
# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
