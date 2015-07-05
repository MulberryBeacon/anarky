#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
General project information.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# ----------------------------------------------------------------------------------------------------------------------
from os.path import basename, join, splitext


# Project information
# ----------------------------------------------------------------------------------------------------------------------
__author__ = 'Eduardo Ferreira'
__version__ = '0.1.4'
__license__ = 'MIT'


# Constants :: Error messages
# ----------------------------------------------------------------------------------------------------------------------
ERROR_INTERRUPTED = 'The program execution was interrupted!'
ERROR_INVALID_FILE = 'The file \'{0}\' either doesn\'t exist or you don\'t have the necessary privileges to access it!'
ERROR_INVALID_DIRECTORY = 'The directory \'{0}\' either doesn\'t exist or you don\'t have the necessary privileges to access it!'
ERROR_INVALID_ENTRY = 'The filesystem entry \'{0}\' either doesn\'t exist or you don\'t have the necessary privileges to access it!'
ERROR_NO_FILES_GIVEN = 'You didn\'t add any files!'
ERROR_WRONG_FILE_TYPE = 'The file \'{0}\' is not a valid {1} file!'
WARNING_NO_JSON_FILE = 'No JSON file with ID3 tags was found. Proceeding with encoding operation without tags.'


# Methods :: Text manipulation
# ----------------------------------------------------------------------------------------------------------------------
def is_string_empty(string):
    """
    Checks if a string is empty.
    """
    return string is None or len(string) == 0


# Methods :: File name management
# ----------------------------------------------------------------------------------------------------------------------
def update_extension(filename, extension=''):
    """
    Updates the extension of the given file.
    If an extension is not provided, the extension from the given file is stripped.
    """
    return splitext(filename)[0] + extension


def update_path(filename, directory, extension):
    """
    Updates the path and extension of the given file.
    """
    # Measure performance for possible solutions
    # return splitext(join(directory, basename(filename)))[0] + extension
    # return join(directory, basename(splitext(filename)[0] + extension))
    return join(directory, splitext(basename(filename))[0] + extension)


# Methods :: Exception handling
# ----------------------------------------------------------------------------------------------------------------------
def keyboard_interrupt():
    print('\n%s\n' % ERROR_INTERRUPTED)
