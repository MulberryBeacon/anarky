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
import unittest


# Test class
# --------------------------------------------------------------------------------------------------
class InterfaceTests(unittest.TestCase):
    def test__file_exists(self):
        with self.assertRaises(TypeError):
            interface.file_exists(None)


# Methods :: Execution and boilerplate
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

