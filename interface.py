#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Common user interface operations.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import section
# -------------------------------------------------------------------------------------------------
from audio import EXTENSIONS, read_tag_file
from collections import defaultdict
from miscellaneous import get_tuple_pairs, tab
import os
import sys

# Constants :: Program version
# -------------------------------------------------------------------------------------------------
VERSION = "0.1.0"

# Constants :: Interface options
# -------------------------------------------------------------------------------------------------
OPTIONS = {
	"help"       : ["-h", "--help", "display this help and exit"],
	"version"    : ["-v", "--version", "output version information and exit"],
	"files"      : ["-f", "--files", "set of individual files to convert"],
	"directory"  : ["-d", "--dir", "directory with a set of files to convert"],
	"destination": ["-e", "--dest", "directory in which the generated files will be saved"],
	"cover"      : ["-c", "--cover", "add an image file with a cover"],
	"tags"       : ["-t", "--tags", "add ID3 tags with the main information"],
	"playlist"   : ["-p", "--playlist", "create a playlist file"]
}

# Constants :: Error messages
# -------------------------------------------------------------------------------------------------
ERROR_INTERRUPTED = "The program execution was interrupted!"
ERROR_INVALID_OPTION = "Invalid option -- '{0}'"
ERROR_INVALID_FILE = ("The '{0}' file either doesn't exist or you don't have the necessary " +
					"privileges to access it!")
ERROR_INVALID_DIRECTORY = ("The '{0}' directory either doesn't exist or you don't have the necessary " +
					"privileges to access it!")
ERROR_NO_FILES_GIVEN = "No {0} files were given!"
ERROR_NO_FILES = "No {0} files were found in the {1} directory!"
ERROR_NO_DIRECTORY_GIVEN = "No directory name was given!"
ERROR_ONLY_ONE_FILE = "Only one {0} file is allowed!"
ERROR_WRONG_FILE_TYPE = "The file {0} doesn't have the {1} extension!"


# Methods :: Command line options and instructions
# -------------------------------------------------------------------------------------------------
def get_help(name, extract):
	"""
	Generates the text with the help instructions for a program.
	"""
	print "Usage:", name, "[OPTION] [-fd] [input-files] [-e] [destination]\n"
	for short_option, long_option, description in OPTIONS.values():
		if extract and (short_option in OPTIONS["cover"] or short_option in OPTIONS["tags"]):
			description = description.replace("add", "extract")

		print tab(1) + short_option + ", " + long_option + "\n" + tab(2) + description


def get_version(name):
	"""
	Generates the text with the current version of a program.
	"""
	print name, "version", VERSION, "\n"


def check_option_none(arguments, extract):
	"""
	Validates if no options were defined by the user.
	"""
	if len(arguments) == 1:
		get_version(arguments[0])
		get_help(arguments[0], extract)
		return False

	return True


def check_option_help(arguments, extract):
	"""
	Validates the "-h" option that shows the program usage instructions and available options.
	"""
	if len(arguments) > 1 and arguments[1] in OPTIONS["help"]:
		get_help(arguments[0], extract)
		return False

	return True


def check_option_version(arguments):
	"""
	Validates the "-v" option that shows the program version.
	"""
	if len(arguments) > 1 and arguments[1] in OPTIONS["version"]:
		get_version(arguments[0])
		return False

	return True


def check_option_first_token(arguments):
	"""
	Checks if the first token in the list of command line arguments is a valid option.
	"""
	if len(arguments) > 1 and not is_option(arguments[1]):
		print ERROR_INVALID_OPTION.format(arguments[1])
		return False

	return True


def check_option_destination(directory):
	"""
	Validates the "-e" option that allows a user to specify a destination directory for the generated
	MP3 files.
	"""
	if not directory_exists(directory):
		return None

	return os.path.abspath(directory[0])


def check_option_files(files, extension):
	"""
	Validates the "-f" option that allows a user to specify a list of audio files to convert to another
	format.
	"""
	result = []

	# Goes through the list of file names
	for name in files:
		filename = os.path.abspath(name)

		# Checks if the file exists
		if not os.path.isfile(filename):
			print ERROR_INVALID_FILE.format(name)
			continue

		# Checks if the file has the desired extension
		if not name.endswith(extension):
			print ERROR_WRONG_FILE_TYPE.format(name, extension)
			continue

		result.append(filename)

	# Checks if one or more file names were given
	if len(result) == 0:
		print ERROR_NO_FILES_GIVEN.format(extension)
		return None

	return result


def check_option_directory(directory, extension):
	"""
	Validates the "-d" option that allows a user to specify a directory with audio files to convert to
	another format.
	"""
	# Checks if a single directory name was given and if it's a valid filesystem directory
	if not directory_exists(directory):
		return None

	# Goes through the list of files in the directory
	result = []
	for root, dirs, files in os.walk(directory[0], topdown=False):
		for name in files:
			filename = os.path.join(root, name)

			# Checks if the file has the desired extension
			if not name.endswith(extension):
				print ERROR_WRONG_FILE_TYPE.format(name, extension)
				continue

			result.append(filename)

	# Checks if one or more valid files were found
	if len(result) == 0:
		print ERROR_NO_FILES_GIVEN.format(extension)
		return None

	return result


def check_option_cover(cover):
	"""
	Validates the "-c" option that allows a user to specify an image file with an album cover to insert
	in the converted files.
	"""
	# Checks if a single file name was given
	if len(cover) != 1:
		print ERROR_ONLY_ONE_FILE.format("cover")
		return None

	# Checks if the file exists
	if not os.path.isfile(cover[0]):
		print ERROR_INVALID_FILE.format(cover)
		return None

	return cover[0]


def check_option_tags(tags):
	"""
	Validates the "-t" option that allows a user to specify a file with a set of ID3 tags to insert in
	the converted files.
	"""
	# Checks if a single file name was given
	if len(tags) != 1:
		print ERROR_ONLY_ONE_FILE.format("tag")
		return None

	# Checks if the file exists
	if not os.path.isfile(tags[0]):
		print ERROR_INVALID_FILE.format(tags[0])
		return None

	#return tags[0]
	return read_tag_file(tags[0])


def is_option(token):
	"""
	Checks if a text token is a valid option.
	"""
	if token.startswith("-"):
		for entry in OPTIONS.values():
			if token in entry[0:2]:
				return True

	return False


def split_options(arguments):
	"""
	Goes through the options defined by the user and organizes them in a dictionary.
	"""
	# Filters any valid options and retrieves their index in the arguments list
	tuple_list = [(token, idx) for idx, token in enumerate(arguments) if is_option(token)]
	tuple_pairs = get_tuple_pairs(tuple_list)

	options = defaultdict(list)

	# Goes through the list of tuple pairs
	for current, next in tuple_pairs:
		values = arguments[current[1] + 1: (next[1] if next != None else None)]
		options[current[0]].extend(values)

	return options


def check_options(arguments, extract=False):
	"""
	Checks the full set of command line arguments.
	"""
	# Splits the program name to get the input and output formats
	command = (arguments[0][2:] if arguments[0].startswith("./") else arguments[0])
	(input_format, output_format) = command.split("2")

	# Checks the set of information options
	if (not check_option_none(arguments, extract)
		or not check_option_help(arguments, extract)
		or not check_option_version(arguments)):
		sys.exit()

	# Default values for the return values
	files = []
	destination = os.getcwd()
	cover = (False if extract else "")
	tags = (False if extract else {})
	playlist = False

	# Pre-processes the option list
	options = split_options(arguments[1:])

	# Goes through the list of options
	for option, values in options.items():

		# Option "-e"
		if option in OPTIONS["destination"]:
			destination = check_option_destination(values)
			if destination == None:
				sys.exit()

		# Option "-c"
		elif option in OPTIONS["cover"]:
			if extract:
				cover = True
			else:
				cover = check_option_cover(values)
				if cover == None:
					sys.exit()

		# Option "-t"
		elif option in OPTIONS["tags"]:
			if extract:
				tags = True;
			else:
				tags = check_option_tags(values)
				if tags == None:
					sys.exit()

		# Option "-p"
		elif option in OPTIONS["playlist"]:
			playlist = True

		else:
			# Option "-f"
			if option in OPTIONS["files"]:
				file_list = check_option_files(values, EXTENSIONS[input_format])

			# Option "-d"
			elif option in OPTIONS["directory"]:
				file_list = check_option_directory(values, EXTENSIONS[input_format])

			if file_list == None:
				sys.exit()

			files.extend(file_list)

	return (files, destination, cover, tags, playlist)


# Methods :: Directory and file library
# -------------------------------------------------------------------------------------------------
def directory_exists(directory):
	"""
	Checks if a directory exists.
	"""
	# Checks if a single directory name was given
	if len(directory) != 1:
		print ERROR_NO_DIRECTORY_GIVEN
		return False

	# Checks if the given directory name is a valid filesystem directory
	if not os.path.isdir(directory[0]):
		print ERROR_INVALID_DIRECTORY.format(directory[0])
		return False

	return True
