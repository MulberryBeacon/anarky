#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Common user interface operations.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# --------------------------------------------------------------------------------------------------
from os import walk
from os.path import isdir, isfile, join

import argparse
import logging
import sys


# Constants
# --------------------------------------------------------------------------------------------------
ERROR = "{} '{}' is not available (doesn't exist or no privileges to access it)!"
ERROR_INVALID = "{} '{}' is invalid!"


# Project information
# --------------------------------------------------------------------------------------------------
__author__ = 'Eduardo Ferreira'
__version__ = '0.0.2'
__license__ = 'MIT'


# Logger
# --------------------------------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


# Methods :: File system library
# --------------------------------------------------------------------------------------------------
def file_exists(filename):
    """
    Checks if a file is a valid file system entry.
    :param filename: The name of a file
    :return: True if the given file name matches an actual file; False otherwise
    """
    try:
        if not isfile(filename):
            _logger.error(ERROR.format('File', filename))
    except TypeError:
        _logger.error(ERROR_INVALID.format('File', filename))
    finally:
        return False

    return True


def directory_exists(directory):
    """
    Checks if a directory is a valid filesystem entry.
    :param directory: The name of a directory
    :return: True if the given directory name matches an actual directory; False otherwise
    """
    try:
        if not isdir(directory):
            _logger.error(ERROR.format('Directory', directory))
    except TypeError:
        _logger.error(ERROR_INVALID.format('Directory', filename))
    finally:
        return False

    return True


def get_input_files(entries):
    """
    Checks and stores the input files provided in the command line interface.
    :param entries: The set of input entries (can be either files or directories)
    :return: A complete list of the input files
    """
    result = []
    try:
        for entry in entries:
            if isfile(entry):
                result.append(entry)
            elif isdir(entry):
                for root, directories, files in walk(entry):
                    for filename in files:
                        file_path = join(root, filename)
                        result.append(file_path)
            else:
                _logger.error(ERROR.format('File system entry', entry))
    except TypeError:
        _logger.error(ERROR.format('', entry))

    return result


# Methods :: Command line options and instructions
# --------------------------------------------------------------------------------------------------
def parse_options(program, description, decode=False):
    """
    Parses and retrieves the values for the full set of command line arguments.
    :param program: The name of the program
    :param description: The description of the program
    :param decode: Flag the indicates if it's an encoding or decoding operation
    :return: The list of command line arguments
    """
    # Defines the parent parser
    parser = argparse.ArgumentParser(prog=program, description=description)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    # TODO: keeping only the parameters for input files and output location because they will only
    # be tackled in a future version
    #parser.add_argument('-p', '--playlist', action='store_true', default='False',
    #    help='create playlist file')
    #tags_help = '{} ID3 tags'.format('extract' if decode else 'add')
    #parser.add_argument('-t', '--tags', action='store_true', help=tags_help)
    #cover_help = '{} album art'
    #if decode:
    #    parser.add_argument('-c', '--cover', action='store_true',
    #        help=cover_help.format('extract'))
    #else:
    #    parser.add_argument('-c', '--cover', metavar='IMG', dest='cover',
    #        help=cover_help.format('add'))    

    group = parser.add_argument_group('options')
    group.add_argument('-f', '--files', nargs='+', metavar='FILES', dest='input_files',
        help='input files', required=True)
    # TODO: the destination probably shouldn't be a required parameter. And the name could be
    # changed to "output"...
    group.add_argument('-o', '--output', metavar='OUTPUT', dest='output_dir', help='output directory')

    return parser.parse_args()


def get_options(program, description, decode=False):
    """
    Parses, retrieves and validates the values for the full set of command line arguments.
    :param program: The name of the program
    :param description: The description of the program
    :param decode: Flag the indicates if it's an encoding or decoding operation
    :return: The fully parsed and validated list of command line arguments
    """
    args = parse_options(program, description, decode)

    # Checks the input files
    files = get_input_files(args.input_files)
    if len(files) == 0:
        _logger.error('No files were provided!')
        sys.exit(1)

    # TODO: this bit needs to be completely reviewed!
    # Checks the output directory, cover and tag parameters 
    if not (directory_exists(args.output_dir) and not (
            not decode and args.cover is not None and not file_exists(args.cover))):
        sys.exit(1)

    return files, args.output_dir, args.cover, args.tags, args.playlist

