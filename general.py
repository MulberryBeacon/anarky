#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
General project information.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Project information
# ----------------------------------------------------------------------------------------------------------------------
__author__ = 'Eduardo Ferreira'
__version__ = '0.0.4'
__license__ = 'MIT'


# Methods :: Text manipulation
# ----------------------------------------------------------------------------------------------------------------------
def is_string_empty(string):
	"""
	Checks if a string is empty.
	"""
	return string is None or len(string) == 0
