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

	return TAB + indent_text_rec(number - 1)


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
# Checks if a file exists and has the given extension.
#
# @param filename File to check
# @param extension File extension
# @return True if the file exists and has the given extension; False otherwise
# *************************************************************************************************
def file_exists(filename, extension=""):
	file_path = os.path.abspath(filename)
	if os.path.isfile(file_path) and file_path.endswith(extension):
		return True

	return False


# *************************************************************************************************
# Checks if a folder contains, at least, one file with the given extension.
#
# @param folder Folder to check for files
# @param extension File extension
# @return True if the folder contains any files with the given extension; False otherwise
# *************************************************************************************************
def folder_has_files(folder, extension=""):
	for item in os.listdir(folder):
		if file_exists(item, extension):
			return True

	return False


# *************************************************************************************************
# Extracts the names of the files in the given folders.
#
# @param folders List of folders
# @param extension File extension
# @return A list of file names
# *************************************************************************************************
def extract_files(folders, extension=""):
	files = []
	for folder in folders:
		for item in os.listdir(folder):
			if file_exists(item, extension):
				files.append(item)

	return files


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

	# Checks if a single folder name was given
	if len(folder) != 1:
		print ERROR_NO_FOLDER_GIVEN
		return False

	# Checks if the given folder name is a valid filesystem folder
	if not os.path.isdir(folder[0]):
		print ERROR_INVALID_FOLDER.format(folder[0])
		return False

	return True


# *************************************************************************************************
# Validates the "-f" option that allows a user to specify a list of FLAC files to convert to MP3.
#
# @param files List of file names
# @return True if the program should continue its execution; False otherwise
# *************************************************************************************************
def check_option_somefiles(files):

	# Checks if one or more file names were given
	if len(files) == 0:
		print ERROR_NO_FILES_GIVEN
		return False

	# Goes through the list of file names
	for filename in files:
		if not file_exists(filename, audiolib.EXT_FLAC):
			print ERROR_INVALID_FILE.format(filename)
			return False

	return True


# *************************************************************************************************
# Validates the "-F" option that allows a user to specify a list of folders with FLAC files to
# convert to MP3.
#
# @return True if the program should continue its execution; False otherwise
# *************************************************************************************************
def check_option_allfiles(folders):

	# Checks if one or more folder names were given
	if len(folder) == 0:
		print ERROR_NO_FOLDER_GIVEN
		return False

	# Goes through the list of folders and checks if each one contains, at least, one file with the
	# FLAC extension
	for folder in folders:
		if not folder_has_files(folder, audiolib.XT_FLAC):
			print ERROR_NO_FILES.format(audiolib.EXT_FLAC, folder)
			return False

	return True


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

	# Goes through the list of options
	for option, values in options.items():

		# Option "-d"
		if option == OPTIONS["directory"]:
			if not check_option_folder(values):
				sys.exit()

			destination = os.path.abspath(values[0])

		# Option "-f"
		elif option == OPTIONS["somefiles"]:
			if not check_option_somefiles(values):
				sys.exit()

			files.extend(values)

		# Option "-F"
		elif option == OPTIONS["allfiles"]:
			if not check_option_allfiles():
				sys.exit()

			files.extend(extract_files(values, audiolib.EXT_FLAC))

	# Runs the main workflow for each FLAC file
	for item in files:
		tags = audiolib.decode_flac(item)
		audiolib.encode_wav_flac(item, tags)
		audiolib.encode_wav_mp3(item, tags, destination)
		audiolib.cleanup(item)


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
