#!/usr/bin/python -tt

# Module import section
# -------------------------------------------------------------------------------------------------
from collections import defaultdict
from miscellaneous import get_tuple_pairs
import os


# Constants :: Lists
# -------------------------------------------------------------------------------------------------
OPTIONS = {"help": "-h", "version": "-v", "somefiles": "-f", "allfiles": "-F", "directory": "-d"}


# Constants :: Error messages
# -------------------------------------------------------------------------------------------------
ERROR_INVALID_OPTION = "Invalid option -- '{0}'"
ERROR_INVALID_FILE = ("The '{0}' file either doesn't exist or you don't have the necessary " +
					"privileges to access it!")
ERROR_INVALID_FOLDER = ("The '{0}' folder either doesn't exist or you don't have the necessary " +
					"privileges to access it!")
ERROR_NO_FILES_GIVEN = "No FLAC files were given!"
ERROR_NO_FILES = "No {0} files were found in the {1} folder!"
ERROR_NO_FOLDER_GIVEN = "No folder name was given!"
ERROR_WRONG_FILE_TYPE = "The file {0} doesn't have the {1} extension!"


# Methods :: Command line options and instructions
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Validates if no options were defined by the user.
#
# @param arguments List of command line arguments
# @param version Program version text
# @param help Program help text
# @return True if the program should continue its execution; False otherwise
# *************************************************************************************************
def check_option_none(arguments, version, help):
	if len(arguments) == 1:
		print version
		print help
		return False

	return True


# *************************************************************************************************
# Validates the "-h" option that shows the program usage instructions and available options.
#
# @param arguments List of command line arguments
# @param help Program help text
# @return True if the program should continue its execution; False otherwise
# *************************************************************************************************
def check_option_help(arguments, help):
	if len(arguments) > 1 and arguments[1] == OPTIONS["help"]:
		print help
		return False

	return True


# *************************************************************************************************
# Validates the "-v" option that shows the program version.
#
# @param arguments List of command line arguments
# @param version Program version text
# @return True if the program should continue its execution; False otherwise
# *************************************************************************************************
def check_option_version(arguments, version):
	if len(arguments) > 1 and arguments[1] == OPTIONS["version"]:
		print version
		return False

	return True


# *************************************************************************************************
# Checks if the first token in the list of command line arguments is a valid option.
#
# @param arguments List of command line arguments
# @return True if the program should continue its execution; False otherwise
# *************************************************************************************************
def check_option_first_token(arguments):
	if len(arguments) > 1 and not is_option(arguments[1]):
		print ERROR_INVALID_OPTION.format(arguments[1])
		return False

	return True


# *************************************************************************************************
# Validates the "-d" option that allows a user to specify a destination folder for the generated
# MP3 files.
#
# @param folder Destination folder name
# @return True if the program should continue its execution; False otherwise
# *************************************************************************************************
def check_option_folder(folder):

	# Checks if a single folder name was given and if it's a valid filesystem folder
	if not folder_exists(folder):
		return None

	return os.path.abspath(folder[0])


# *************************************************************************************************
# Validates the "-f" option that allows a user to specify a list of audio files to convert to
# another format.
#
# @param files List of file names
# @return True if the program should continue its execution; False otherwise
# *************************************************************************************************
def check_option_somefiles(files, extension):
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
		print ERROR_NO_FILES_GIVEN
		return None

	return result


# *************************************************************************************************
# Validates the "-F" option that allows a user to specify a folder with audio files to convert to
# another format.
#
# @return True if the program should continue its execution; False otherwise
# *************************************************************************************************
def check_option_allfiles(folder, extension):

	# Checks if a single folder name was given and if it's a valid filesystem folder
	if not folder_exists(folder):
		return None

	# Goes through the list of files in the folder
	result = []
	for root, dirs, files in os.walk(folder[0], topdown=False):
		for name in files:
			filename = os.path.join(root, name)

			# Checks if the file has the desired extension
			if not name.endswith(extension):
				print ERROR_WRONG_FILE_TYPE.format(name, extension)
				continue

			result.append(filename)

	# Checks if one or more valid files were found
	if len(result) == 0:
		print ERROR_NO_FILES_GIVEN
		return None

	return result


# *************************************************************************************************
# Checks if a text token is a valid option.
#
# @param token Text token
# @return True if the token is a valid option; False otherwise
# *************************************************************************************************
def is_option(token):
	return token.startswith("-") and token in OPTIONS.values()


# *************************************************************************************************
# Goes through the options defined by the user and organizes them in a dictionary.
#
# @param arguments List of command line arguments
# @return A dictionary with the options set by the user
# *************************************************************************************************
def split_options(arguments):

	# Filters any valid options and retrieves their index in the arguments list
	tuple_list = [(token, idx) for idx, token in enumerate(arguments) if is_option(token)]
	tuple_pairs = get_tuple_pairs(tuple_list)

	options = defaultdict(list)

	# Goes through the list of tuple pairs
	for current, next in tuple_pairs:
		values = arguments[current[1] + 1: (next[1] if next != None else None)]
		options[current[0]].extend(values)

	return options


# Methods :: Folder and file library
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Checks if a folder exists.
#
# @param folder Folder name
# @return True if the program should continue its execution; False otherwise
# *************************************************************************************************
def folder_exists(folder):

	# Checks if a single folder name was given
	if len(folder) != 1:
		print ERROR_NO_FOLDER_GIVEN
		return False

	# Checks if the given folder name is a valid filesystem folder
	if not os.path.isdir(folder[0]):
		print ERROR_INVALID_FOLDER.format(folder[0])
		return False

	return True
