#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
General project information.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# ----------------------------------------------------------------------------------------------------------------------
from os.path import basename, isdir, isfile, join, splitext


# Project information
# ----------------------------------------------------------------------------------------------------------------------
__author__ = 'Eduardo Ferreira'
__version__ = '0.1.4'
__license__ = 'MIT'


# Constants :: Error messages
# ----------------------------------------------------------------------------------------------------------------------
ERROR_INVALID_FILE = ("The '{0}' file either doesn't exist or you don't have the necessary " +
					"privileges to access it!")
ERROR_INVALID_DIRECTORY = ("The '{0}' directory either doesn't exist or you don't have the necessary " +
					"privileges to access it!")


# Methods :: Text manipulation
# ----------------------------------------------------------------------------------------------------------------------
def is_string_empty(string):
	"""
	Checks if a string is empty.
	"""
	return string is None or len(string) == 0


# Methods :: File name management
# ----------------------------------------------------------------------------------------------------------------------
def file_strip_ext(filename):
	"""
	Strips the extension from the given file.
	"""
	return splitext(filename)[0]


def file_strip_full(filename):
	"""
	Strips the path and extension from the given file.
	"""
	return splitext(basename(filename))[0]


def file_update_ext(filename, extension):
	"""
	Updates the extension of the given file.
	"""
	return splitext(filename)[0] + extension


def file_update_full(filename, directory, extension):
	"""
	Updates the path and extension of the given file.
	"""
	# Measure performance for possible solutions
	#return splitext(join(directory, basename(filename)))[0] + extension
	#return join(directory, basename(splitext(filename)[0] + extension))
	return join(directory, splitext(basename(filename))[0] + extension)


# Methods :: Directory and file library
# -------------------------------------------------------------------------------------------------
def file_exists(filename):
	"""
	Checks if a file is a valid filesystem entry.
	"""
	if not isfile(filename):
		print ERROR_INVALID_FILE.format(filename)
		return False

	return True


def directory_exists(directory):
	"""
	Checks if a directory is a valid filesystem entry.
	"""
	if not isdir(directory):
		print ERROR_INVALID_DIRECTORY.format(directory)
		return False

	return True
