#!/usr/bin/python -tt

# Module import section
# -------------------------------------------------------------------------------------------------
from collections import defaultdict
from itertools import tee, islice, chain, izip
from subprocess import call, PIPE, Popen
import os
import sys


# Constants :: Lists and file extensions
# -------------------------------------------------------------------------------------------------
OPTIONS = {"help": "-h", "version": "-v", "somefiles": "-f", "directory": "-d", "allfiles": "-F"}
TAG_NAMES = ["TITLE", "ARTIST", "ALBUM", "DATE", "TRACKNUMBER", "TRACKTOTAL", "GENRE"]
TAG_FLAGS = ["--tt", "--ta", "--tl", "--ty", "--tn", "--tg"]
EXT_FLAC = ".flac"
EXT_MP3 = ".mp3"
EXT_WAV = ".wav"


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


# Constants :: Information messages
# -------------------------------------------------------------------------------------------------
INFO_HELP = ("Usage: flactomp3 [-f] [filenames] [-d] [folder]\n" +
			"    -f\n        specify a set of files to convert\n" +
			"    -d\n        folder in which the generated MP3 files will be saved\n" +
			"    -h\n        display this help and exit\n" +
			"    -v\n        output version information and exit\n")

INFO_VERSION = "flactomp3 version 0.1.0\n"


# Methods :: File encoding and decoding
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Retrieves and stores the ID3 tag values of a FLAC audio file.
#
# @param filename FLAC audio file name
# @return The values of the metatags
# *************************************************************************************************
def get_tags(filename):
	tag_values = []
	for tag_name in TAG_NAMES:

		# Prepares the 'sed' program arguments
		sed = ["sed", "s/.*=//"]

		# Invokes the 'metaflac' and 'sed' programs to retrieve the ID3 tag values
		p1 = Popen(["metaflac", "--show-tag=" + tag_name, filename], stdout=PIPE)
		p2 = Popen(sed, stdin=p1.stdout, stdout=PIPE)
		tag_values.append(p2.communicate()[0].rstrip("\n"))

	return tag_values


# *************************************************************************************************
# Decodes a FLAC audio file, generating the corresponding WAV audio file and storing its ID3 tags.
#
# @param filename FLAC audio file name
# @return The values of the metatags
# *************************************************************************************************
def decode_flac(filename):

	# Prepares the 'flac' program arguments:
	# -d => Decode (the default behavior is to encode)
	# -f => Force overwriting of output files
	flac = ["flac", "-d", "-f", filename]

	# Invokes the 'flac' program to decode the FLAC audio file and retrieves the ID3 tags
	call(flac)
	tag_values = get_tags(filename)

	return tag_values


# *************************************************************************************************
# Encodes a WAV audio file, generating the corresponding FLAC audio file and storing its ID3 tags.
#
# @param filename WAV audio file name
# @param tag_values Values of the ID3 tags
# *************************************************************************************************
def encode_wav_flac(filename, tag_values):

	# Prepares the ID3 tags to be passed as parameters of the 'flac' program
	id3_flags = ["-T", "TITLE=" + tag_values[0], "-T", "ARTIST=" + tag_values[1], "-T", "ALBUM=" +
				tag_values[2], "-T", "DATE=" + tag_values[3], "-T", "TRACKNUMBER=" + tag_values[4],
				"-T", "TRACKTOTAL=" + tag_values[5], "-T", "GENRE=" + tag_values[6]]

	# Prepares the 'flac' program arguments:
	# -f => Force overwriting of output files
	# -8 => Synonymous with -l 12 -b 4096 -m -e -r 6
	# -V => Verify a correct encoding
	flac = ["flac", "-f8V"]
	flac.extend(id3_flags)

	# Replaces the extension of the input file (from FLAC to WAV)
	flac.append(os.path.splitext(filename)[0] + EXT_WAV)

	# Invokes the 'flac' program to encode the WAV audio file with the given ID3 tags
	call(flac)


# *************************************************************************************************
# Encodes a WAV audio file, generating the corresponding MP3 audio file and storing its ID3 tags.
#
# @param filename WAV audio file name
# @param tag_values Values of the ID3 tags
# @param destination Destination folder where the resulting MP3 file will be stored
# *************************************************************************************************
def encode_wav_mp3(filename, tag_values, destination=""):

	# Prepares the ID3 tags to be passed as parameters of the 'lame' program
	id3_flags = ["--tt", tag_values[0], "--ta", tag_values[1], "--tl", tag_values[2],
				"--ty", tag_values[3], "--tn", tag_values[4] + "/" + tag_values[5],
				"--tg", tag_values[6]]

	# Prepares the 'lame' program arguments:
	# -b 320          => Set the bitrate to 320 kbps
	# -q 0            => Highest quality, very slow
	# --preset insane => Type of the quality settings
	# --id3v2-only    => Add only a version 2 tag
	lame = ["lame", "-b", "320", "-q", "0", "--preset", "insane", "--id3v2-only"]
	lame.extend(id3_flags)

	# Replaces the extension of the input file (from FLAC to WAV)
	lame.append(os.path.splitext(filename)[0] + EXT_WAV)

	# Updates the path of the output file to match the given destination folder and replaces its
	# extension (from FLAC to MP3)
	new_filename = os.path.basename(filename)
	new_filename = os.path.splitext(new_filename)[0]
	new_filename = os.path.join(destination, new_filename)
	lame.append(new_filename + EXT_MP3)

	# Invokes the 'lame' program to encode the WAV audio file with the given ID3 tags
	# FLAC => WAV => MP3
	call(lame)


# *************************************************************************************************
# Implements the main workflow for converting a single FLAC file into MP3.
#
# @param filename FLAC audio file name
# @param destination Destination folder where the resulting MP3 file will be stored
# *************************************************************************************************
def workflow(filename, destination):
	tags = decode_flac(filename)
	encode_wav_flac(filename, tags)
	encode_wav_mp3(filename, tags, destination)
	cleanup(filename)


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


# *************************************************************************************************
# Removes the temporary WAV audio file created during the conversion process.
#
# @param filename File to remove
# *************************************************************************************************
def cleanup(filename):

	# Prepares the 'rm' program arguments:
	# -r => Remove directories and their contents recursively
	# -f => Ignore nonexistent files, never prompt
	rm = ["rm", "-rf"]

	# Replaces the extension of the input file (from FLAC to WAV)
	rm.append(os.path.splitext(filename)[0] + EXT_WAV)

	# Invokes the 'rm' program to remove the temporary WAV audio file
	call(rm)


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
		if not file_exists(filename, EXT_FLAC):
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
		if not folder_has_files(folder, EXT_FLAC):
			print ERROR_NO_FILES.format(EXT_FLAC, folder)
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

			files.extend(extract_files(values, EXT_FLAC))

	# Runs the workflow for each file
	for item in files:
		workflow(item, destination)


# *************************************************************************************************
# Main function
# *************************************************************************************************
def main():
	run(sys.argv)


# Standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()
