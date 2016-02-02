#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Common user interface operations.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# ----------------------------------------------------------------------------------------------------------------------
from general import __version__, ERROR_INVALID_ENTRY, ERROR_INVALID_FILE, ERROR_INVALID_DIRECTORY, ERROR_NO_FILES_GIVEN
from os import listdir, walk
from os.path import isdir, isfile, join

import argparse
import sys


# Methods :: File system library
# ----------------------------------------------------------------------------------------------------------------------
def file_exists(filename):
    """
    Checks if a file is a valid filesystem entry.
    """
    if not isfile(filename):
        print(ERROR_INVALID_FILE.format(filename))
        return False

    return True


def directory_exists(directory):
    """
    Checks if a directory is a valid filesystem entry.
    """
    if not isdir(directory):
        print(ERROR_INVALID_DIRECTORY.format(directory))
        return False

    return True


def get_input_files(input_files):
    """
    Checks and stores the input files provided in the command line interface.
    """
    result = []
    for entry in input_files:
        if isfile(entry):
            result.append(entry)
        elif isdir(entry):
            for root, directories, files in walk(entry):
                for filename in files:
                    file_path = join(root, filename)
                    result.append(file_path)
        else:
            print(ERROR_INVALID_ENTRY.format(name))

    return result


# Methods :: Command line options and instructions
# ----------------------------------------------------------------------------------------------------------------------
def parse_options(program, description, decode=False):
    """
    Parses and retrieves the values for the full set of command line arguments.
    """
    # Defines the parent parser
    parser = argparse.ArgumentParser(prog=program, description=description)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-p', '--playlist', action='store_true', default='False', help='create playlist file')
    tags_help = '%s ID3 tags' % ('extract' if decode else 'add')
    parser.add_argument('-t', '--tags', action='store_true', default='False', help=tags_help)
    cover_help = '{0} album art'
    if decode:
        parser.add_argument('-c', '--cover', action='store_true', help=cover_help.format('extract'))
    else:
        parser.add_argument('-c', '--cover', metavar='IMG', dest='cover', help=cover_help.format('add'))    

    group = parser.add_argument_group('options')
    group.add_argument('-f', '--files', nargs='+', metavar='FILES', dest='input_files', help='input files to convert', required=True)
    group.add_argument('-d', '--dest', metavar='DEST', dest='output_dir', help='output directory for the generated files', required=True)

    return parser.parse_args()


def get_options(program, description, decode=False):
    """
    Parses, retrieves and validates the values for the full set of command line arguments.
    """
    args = parse_options(program, description, decode)

    # Checks the input files
    files = get_input_files(args.input_files)
    if len(files) == 0:
        print(ERROR_NO_FILES_GIVEN)
        sys.exit()

    # Checks the output directory, cover and tag parameters 
    if not directory_exists(args.output_dir) \
        or (not decode and not args.cover is None and not file_exists(args.cover)):
        sys.exit()

    return (files, args.output_dir, args.cover, args.tags, args.playlist)
