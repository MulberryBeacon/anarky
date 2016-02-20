#!/usr/bin/python
# -*- coding: utf8 -*-

"""
General project information.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# ----------------------------------------------------------------------------------------------------------------------
from os.path import basename, join, splitext
import logging


# Logger
# ----------------------------------------------------------------------------------------------------------------------
_logger = logging.getLogger(__name__)


# Constants :: Error messages
# ----------------------------------------------------------------------------------------------------------------------
WARNING_NO_JSON_FILE = 'No JSON file with ID3 tags was found. Proceeding with encoding operation without tags.'


# Methods :: Text manipulation
# ----------------------------------------------------------------------------------------------------------------------
def is_string_empty(string):
    """
    Checks if a string is empty.
    :param string: The string to check
    :return: True if the string is empty; False otherwise
    """
    return string is None or len(string) == 0


# Methods :: File name management
# ----------------------------------------------------------------------------------------------------------------------
def update_extension(filename, extension=''):
    """
    Updates the extension of the given file.
    If an extension is not provided, the extension from the given file is stripped.
    :param filename: The name of the file
    :param extension: The file extension
    :return: The name of the file updated with the given extension
    """
    return splitext(filename)[0] + extension


def update_path(filename, directory, extension):
    """
    Updates the path and extension of the given file.
    :param filename: The name of the file
    :param directory: The directory
    :param extension: The file extension
    :return: The name of the file updated with the given directory and extension
    """
    # TODO: Measure performance for possible solutions
    # return splitext(join(directory, basename(filename)))[0] + extension
    # return join(directory, basename(splitext(filename)[0] + extension))
    return join(directory, splitext(basename(filename))[0] + extension)


# Methods :: Exception handling
# ----------------------------------------------------------------------------------------------------------------------
def keyboard_interrupt():
    _logger.warn('\nThe program execution was interrupted!\n')
