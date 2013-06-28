#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Common user interface operations.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import section
# ----------------------------------------------------------------------------------------------------------------------
import general

import argparse
import os
import sys

# Constants :: Error messages
# ----------------------------------------------------------------------------------------------------------------------
ERROR_INTERRUPTED = "The program execution was interrupted!"
ERROR_INVALID_FILE = ("The '{0}' file either doesn't exist or you don't have the necessary " +
					"privileges to access it!")
ERROR_INVALID_DIRECTORY = ("The '{0}' directory either doesn't exist or you don't have the necessary " +
					"privileges to access it!")
ERROR_WRONG_FILE_TYPE = "The file {0} doesn't have the {1} extension!"

# Methods :: Command line options and instructions
# ----------------------------------------------------------------------------------------------------------------------
def check_options(program, description, extension):
	"""
	Checks the full set of command line arguments.
	"""
	parser = argparse.ArgumentParser(prog=program, description=description, add_help=False)
	group = parser.add_argument_group("Options")
	group.add_argument("-h", "--help", action="help", help="show this help message and exit")
	group.add_argument("-v", "--version", action="version", version="%(prog)s " + general.__version__)
	group.add_argument("-f", "--files", nargs="+", metavar="FILE", dest="input_files", help="set of files to convert", required=True)
	group.add_argument("-d", "--dest", metavar="DEST", dest="output_dir", help="directory in which the generated files will be saved", required=True)
	group.add_argument("-c", "--cover", metavar="IMG", dest="cover", help="add an image file with a cover")
	group.add_argument("-t", "--tags", metavar="TAGS", dest="tags", help="add ID3 tags with the main information")
	group.add_argument("-p", "--playlist", action="store_true", help="create a playlist file")
	args = parser.parse_args()

	files = []

	# Goes through the list of file names
	for name in args.input_files:

		# Checks if the file exists
		if not file_exists(name):
			continue

		# Checks if the file has the desired extension
		if not name.endswith(extension):
			print ERROR_WRONG_FILE_TYPE.format(name, extension)
			continue

		files.append(name)

	# Checks if one or more valid files were given
	if len(files) == 0:
		print ERROR_NO_FILES_GIVEN.format(extension)
		sys.exit()

	# Checks the output directory, cover and tag files
	if not directory_exists(args.output_dir)
		or (not args.cover is None and not file_exists(args.cover))
		or (not args.tags is None and not file_exists(args.tags)):
		sys.exit()

	return files, args.output_dir, args.cover, args.tags, args.playlist


# Methods :: Directory and file library
# -------------------------------------------------------------------------------------------------
def file_exists(filename):
	"""
	Checks if a file is a valid filesystem entry.
	"""
	if not os.path.isfile(filename):
		print ERROR_INVALID_FILE.format(filename)
		return False

	return True


def directory_exists(directory):
	"""
	Checks if a directory is a valid filesystem entry.
	"""
	if not os.path.isdir(directory):
		print ERROR_INVALID_DIRECTORY.format(directory)
		return False

	return True
