#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Common user interface operations.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# ----------------------------------------------------------------------------------------------------------------------
from general import __version__, ERROR_INVALID_FILE, ERROR_INVALID_DIRECTORY, ERROR_NO_FILES_GIVEN
from os import listdir, walk
from os.path import isdir, isfile, join

import argparse
import sys


# Methods :: Directory and file library
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
                    filepath = join(root, filename)
                    result.append(filepath)
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
    group = parser.add_argument_group("options")
    group.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    group.add_argument('-f', '--files', nargs='+', metavar='FILES', dest='input_files', help='set of files to convert', required=True)
    group.add_argument('-d', '--dest', metavar='DEST', dest='output_dir', help='directory in which the generated files will be saved', required=True)
    group.add_argument('-p', '--playlist', action='store_true', help='create a playlist file')
    group.add_argument('-t', '--tags', action='store_true', help='add/extract ID3 tags')

    # Defines the text for the common option in the following child parsers
    cover_text = '\'{0}\' an image file with a cover'

    # Defines the child parser for the FLAC=>WAV and FLAC=>WAV=>MP3 workflows
    decode_parser = argparse.ArgumentParser(parents=[parser], add_help=False)
    decode_parser.add_argument('-c', '--cover', action='store_true', help=cover_text.format('extract'))

    # Defines the child parser for the WAV=>FLAC and WAV=>MP3 workflows
    encode_parser = argparse.ArgumentParser(parents=[parser], add_help=False)
    encode_parser.add_argument('-c', '--cover', metavar='IMG', dest='cover', help=cover_text.format('add'))

    # Checks if the program performs a decoding or encoding operation
    return decode_parser.parse_args() if decode else encode_parser.parse_args()


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
