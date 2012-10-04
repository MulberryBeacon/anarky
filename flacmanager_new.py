#!/usr/bin/python -tt

# Module import section
# -------------------------------------------------------------------------------------------------
from collections import defaultdict
from itertools import tee, islice, chain, izip
from subprocess import call
import audiolib
import os
import sys


# Constants :: Lists
# -------------------------------------------------------------------------------------------------
OPTIONS = {"help": "-h", "version": "-v", "somefiles": "-f", "directory": "-d", "allfiles": "-F"}


# Constants :: Error messages
# -------------------------------------------------------------------------------------------------
ERROR_INVALID_OPTION = "Invalid option -- '{0}'"
ERROR_INVALID_FILE = ("The '{0}' file either doesn't exist or you don't have the necessary " +
					"privileges to access it!")
ERROR_INVALID_FOLDER = ("The '{0}' folder either doesn't exist or you don't have the necessary " +
					"privileges to access it!")
ERROR_NO_FOLDER_GIVEN = "No folder name was given!"
ERROR_NO_FILES_GIVEN = "No FLAC files were given!"
ERROR_NO_FILES = "No {0} files were found in the {1} folder!"
ERROR_INTERRUPTED = "The program execution was interrupted!"
ERROR_WRONG_FILE_TYPE = "The file {0} doesn't have the {1} extension!"


# Constants :: Text formatting
# -------------------------------------------------------------------------------------------------
TAB = "    "


# *************************************************************************************************
# Inserts the equivalent of a tab in a string (incremental implementation).
#
# @param number Number of tabs
# @return The concatenation of 'number' occurrences of the tab string
# *************************************************************************************************
def indent(number):
	if (number <= 0):
		return ""

	text = ""
	for i in range(0, number):
		text += TAB

	return text


# *************************************************************************************************
# Inserts the equivalent of a tab in a string (recursive implementation).
#
# @param number Number of tabs
# @return The concatenation of 'number' occurrences of the tab string
# *************************************************************************************************
def indent_rec(number):
	if (number <= 0):
		return ""

	if (number == 1):
		return TAB

	return TAB + indent_rec(number - 1)


# Constants :: Information messages
# -------------------------------------------------------------------------------------------------
INFO_HELP = ("Usage: flactomp3 [-f] [filenames] [-d] [folder]\n" +
			indent(1) + "-f\n" + indent(2) + "specify a set of files to convert\n" +
			indent(1) + "-F\n" + indent(2) + "folder with a set of files to convert\n" +
			indent(1) + "-d\n" + indent(2) + "folder in which the generated MP3 files will be saved\n" +
			indent(1) + "-h\n" + indent(2) + "display this help and exit\n" +
			indent(1) + "-v\n" + indent(2) + "output version information and exit\n")

INFO_VERSION = "flactomp3 version 0.1.1\n"


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


# Methods :: Command line options and instructions
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Validates if no options were defined by the user.
#
# @param arguments List of command line arguments
# @return True if the program should continue its execution; False otherwise
# *************************************************************************************************
def check_option_none(arguments):
	if len(arguments) == 1:
		print INFO_VERSION
		print INFO_HELP
		return False

	return True


# *************************************************************************************************
# Validates the "-h" option that shows the program usage instructions and available options.
#
# @param arguments List of command line arguments
# @return True if the program should continue its execution; False otherwise
# *************************************************************************************************
def check_option_help(arguments):
	if len(arguments) > 1 and arguments[1] == OPTIONS["help"]:
		print INFO_HELP
		return False

	return True


# *************************************************************************************************
# Validates the "-v" option that shows the program version.
#
# @param arguments List of command line arguments
# @return True if the program should continue its execution; False otherwise
# *************************************************************************************************
def check_option_version(arguments):
	if len(arguments) > 1 and arguments[1] == OPTIONS["version"]:
		print INFO_VERSION
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
# Validates the "-f" option that allows a user to specify a list of FLAC files to convert to MP3.
#
# @param files List of file names
# @return True if the program should continue its execution; False otherwise
# *************************************************************************************************
def check_option_somefiles(files):
	result = []

	# Goes through the list of file names
	for name in files:
		filename = os.path.abspath(name)

		# Checks if the file exists
		if not os.path.isfile(filename):
			print ERROR_INVALID_FILE.format(name)
			continue

		# Checks if the file has the desired extension (.flac)
		if not name.endswith(audiolib.EXT_FLAC):
			print ERROR_WRONG_FILE_TYPE.format(name, audiolib.EXT_FLAC)
			continue

		result.append(filename)

	# Checks if one or more file names were given
	if len(result) == 0:
		print ERROR_NO_FILES_GIVEN
		return None

	return result


# *************************************************************************************************
# Validates the "-F" option that allows a user to specify a folder with FLAC files to convert to
# MP3.
#
# @return True if the program should continue its execution; False otherwise
# *************************************************************************************************
def check_option_allfiles(folder):

	# Checks if a single folder name was given and if it's a valid filesystem folder
	if not folder_exists(folder):
		return None

	result = []

	# Goes through the list of files in the folder
	for root, dirs, files in os.walk(folder, topdown=False):
		for name in files:
			filename = os.path.join(root, name)

			# Checks if the file has the desired extension (.flac)
			if not name.endswith(extension):
				print ERROR_WRONG_FILE_TYPE.format(name, audiolib.EXT_FLAC)
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
# Goes through a list of tuples and pairs them.
# As an example, consider the following list of tuples:
# [(A1,A2), (B1,B2), (C1,C2)]
#
# The resulting list of pairs will be:
# [((A1,A2), (B1,B2)), ((B1,B2), (C1,C2)), ((C1,C2), None)]
#
# @param tuple_list List of tuples
# @return A list of pairs of tuples
# *************************************************************************************************
def get_tuple_pairs(tuple_list):
	current, next = tee(tuple_list, 2)
	next = chain(islice(next, 1, None), [None])
	return izip(current, next)


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


# Methods :: Execution and boilerplate
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Defines the main workflow of the application
# *************************************************************************************************
def run(arguments):

	# Checks the set of information options
	if (not check_option_none(arguments)
		or not check_option_version(arguments)
		or not check_option_help(arguments)):
		sys.exit()

	# Source file list and destination folder
	files = []
	destination = os.getcwd()

	# Pre-processes the option list
	options = split_options(arguments)
	source_flag = False

	# Goes through the list of options
	for option, values in options.items():

		# Option "-d"
		if option == OPTIONS["directory"]:
			destination = check_option_folder(values)
			if destination == None:
				sys.exit()
		else:
			# Option "-f"
			if option == OPTIONS["somefiles"]:
				file_list = check_option_somefiles(values)

			# Option "-F"
			elif option == OPTIONS["allfiles"]:
				file_list = check_option_allfiles(values)

			if file_list == None:
				sys.exit()

			files.extend(file_list)
			source_flag = True

	# Checks if any FLAC files were given
	if not source_flag:
		print ERROR_NO_FILES_GIVEN
		sys.exit()

	# Runs the main workflow for each FLAC file
	cover = None
	#for idx, item in enumerate(files):
	for item in files:

		# Checks if it's the first iteration
		#if idx == 0:
			cover = audiolib.get_cover(item)

		tags = audiolib.decode_flac(item)
		#audiolib.encode_wav_flac(item, tags)
		audiolib.encode_wav_mp3(item, tags, cover, destination)
		audiolib.cleanup(item)

		# Checks if it's the last iteration
		#if idx == len(files) - 1:
		#	cover = audiolib.get_cover(item)


# *************************************************************************************************
# Main function
# *************************************************************************************************
def main():
	try:
		run(sys.argv)
	except KeyboardInterrupt:
		print "\n" + ERROR_INTERRUPTED + "\n"


# Standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()
