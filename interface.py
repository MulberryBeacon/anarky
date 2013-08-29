#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Common user interface operations.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# ----------------------------------------------------------------------------------------------------------------------
from general import __version__, directory_exists, file_exists, ERROR_NO_FILES_GIVEN, ERROR_WRONG_FILE_TYPE

import argparse
import sys


# Methods :: Command line options and instructions
# ----------------------------------------------------------------------------------------------------------------------
def parse_options(program, description, extension, decode=False):
	"""
	Checks the full set of command line arguments.
	"""
	# Defines the parent parser
	parser = argparse.ArgumentParser(prog=program, description=description, version="%(prog)s " + __version__)
	group = parser.add_argument_group("options")
	group.add_argument("-f", "--files", nargs="+", metavar="FILE", dest="input_files", help="set of files to convert", required=True)
	group.add_argument("-d", "--dest", metavar="DEST", dest="output_dir", help="directory in which the generated files will be saved", required=True)

	# Defines the text for the common options in the following child parsers
	cover_text = " an image file with a cover"
	tags_text = " ID3 tags with the main information"

	# Defines the child parsers for decoding and encoding programs
	decode_parser = argparse.ArgumentParser(parents=[parser], add_help=False)
	decode_parser.add_argument("-c", "--cover", action="store_true", help="extract" + cover_text)
	decode_parser.add_argument("-t", "--tags", action="store_true", help="extract" + tags_text)

	encode_parser = argparse.ArgumentParser(parents=[parser], add_help=False)
	encode_parser.add_argument("-c", "--cover", metavar="IMG", dest="cover", help="add" + cover_text)
	encode_parser.add_argument("-t", "--tags", metavar="TAGS", dest="tags", help="add" + tags_text)
	encode_parser.add_argument("-p", "--playlist", action="store_true", help="create a playlist file")

	# Checks if the program performs a decoding or encoding operation
	args = decode_parser.parse_args() if decode else encode_parser.parse_args()

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
	if not directory_exists(args.output_dir) \
		or (not decode and not args.cover is None and not file_exists(args.cover)) \
		or (not decode and not args.tags is None and not file_exists(args.tags)):
		sys.exit()

	params = (files, args.output_dir, args.cover, args.tags)
	if not decode:
		params += (args.playlist,)

	return params
