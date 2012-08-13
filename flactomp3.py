#!/usr/bin/python -tt

# Module import section
# -------------------------------------------------------------------------------------------------
import collections
import errno
import os
import re
import subprocess
import sys


# Constants :: Lists and file extensions
# -------------------------------------------------------------------------------------------------
OPTIONS = {"help": "-h", "version": "-v", "somefiles": "-f", "directory": "-d", "allfiles": "-F"}
TAG_NAMES = ["TITLE", "ARTIST", "ALBUM", "DATE", "TRACKNUMBER", "TRACKTOTAL", "GENRE"]
TAG_FLAGS = ["--tt", "--ta", "--tl", "--ty", "--tn", "--tg"]
EXT_FLAC = ".flac"
EXT_WAV = ".wav"


# Constants :: Error messages
# -------------------------------------------------------------------------------------------------
ERROR_OPTION = "Invalid option -- '{0}'"
ERROR_NO_FILES = "No {0} files were found in the current folder!"
ERROR_FOLDER = ("The {0} folder either doesn't exist or you don't have the necessary privileges " +
				"to access it:\n{1}")
ERROR_NO_FILES_GIVEN = "No FLAC files were given!"
ERROR_NO_FOLDER_GIVEN = "No folder name was given!"


# Constants :: Information messages
# -------------------------------------------------------------------------------------------------
INFO_HELP = ("Usage: flactomp3 [-f] [filenames] [-d] [folder]\n" +
			"    -f\n        specify a set of files to convert\n" +
			"    -d\n        folder in which the generated MP3 files will be saved\n" +
			"    -h\n        display this help and exit\n" +
			"    -v\n        output version information and exit\n")

INFO_VERSION = "flactomp3 version 0.1.0\n"


# Methods :: Command line options and instructions
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Generates a list with the indexes of the used defined input command line arguments.
#
# @param arguments List of command line arguments
# @return List of indexes of the input command line arguments
# *************************************************************************************************
def get_argument_index(arguments):
	index_list = []
	for idx, arg in enumerate(arguments):
		#if re.match("^-[a-zA-Z]$", arg) and arg in OPTIONS.values():
		if arg.startswith("-"):
			if arg in OPTIONS.values():
				index_list.append(idx)
			else:
				print ERROR_OPTION.format(arg)
				return []

	return index_list


# *************************************************************************************************
# Validates the "-d" option that allows a user to specify a destination folder for the generated
# MP3 files.
#
# @param arguments List of command line arguments
# @return The destination folder
# *************************************************************************************************
def folder_option(arguments):

	# Goes through the list of input arguments and looks for the "-d" option
	for arg in arguments:
		if arg == OPTIONS["directory"]:

			# Checks if the option is followed by the destination folder
			index = arguments.index(arg) + 1
			if index == len(arguments) or arguments[index].startswith("-"):
				print ERROR_NO_FOLDER_GIVEN
				sys.exit()

			return arguments[index]

	return null


# Methods :: Folder and file library
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Checks if a folder contains, at least, one file with the given extension.
#
# @param folder Folder to check for files
# @param extension File extension
# @return True if the folder contains any files; False otherwise
# *************************************************************************************************
def folder_has_files(folder, extension=""):
	for item in os.listdir(folder):
		item_path = os.path.join(folder, item)
		if os.path.isfile(item_path) and item.endswith(extension):
			return True

	print ERROR_NO_FILES.format(extension)
	return False


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
		p1 = subprocess.Popen(["metaflac", "--show-tag=" + tag_name, filename], stdout=subprocess.PIPE)
		p2 = subprocess.Popen(sed, stdin=p1.stdout, stdout=subprocess.PIPE)
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
	subprocess.call(flac)
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
	flac.append(filename.rstrip(EXT_FLAC) + EXT_WAV)

	# Invokes the 'flac' program to encode the WAV audio file with the given ID3 tags
	subprocess.call(flac)


# *************************************************************************************************
# Encodes a WAV audio file, generating the corresponding MP3 audio file and storing its ID3 tags.
#
# @param filename WAV audio file name
# @param tag_values Values of the ID3 tags
# *************************************************************************************************
def encode_wav_mp3(filename, tag_values):

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
	lame.append(filename.rstrip(EXT_FLAC) + EXT_WAV)

	# Invokes the 'lame' program to encode the WAV audio file with the given ID3 tags
	# FLAC => WAV => MP3
	subprocess.call(lame)


# *************************************************************************************************
# Implements the main workflow for converting a single FLAC file into MP3.
#
# @param filename FLAC audio file name
# *************************************************************************************************
def workflow(filename):
	tags = decode_flac(flac_file)
	encode_wav_flac(flac_file, tags)
	encode_wav_mp3(flac_file, tags)


# Methods :: Execution and boilerplate
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Defines the main workflow of the application
# *************************************************************************************************
def run(arguments):

	# Checks if no arguments were given
	if len(arguments) == 1:
		print INFO_VERSION
		print INFO_HELP
		sys.exit()

	# Checks if the argument is the help option
	if arguments[1] == OPTIONS["help"]:
		print INFO_HELP
		sys.exit()

	# Checks if the argument is the version option
	if arguments[1] == OPTIONS["version"]:
		print INFO_VERSION
		sys.exit()




	if not check_info_options(arguments):
		sys.exit()

	# Gets the list of indexes of the input command line arguments
	index_list = get_argument_index(sys.argv[1:])
	for idx in index_list:
		print idx
#	if index_list


# *************************************************************************************************
# Main function
# *************************************************************************************************
def main():
	run(sys.argv)


# Standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()
