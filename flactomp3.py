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
OPTIONS = {"help": "--help", "version": "--version", "somefiles": "-f", "directory": "-d",
		"allFiles": "-F"}
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

# Constants :: Information messages
# -------------------------------------------------------------------------------------------------
INFO_OPTIONS = ("No options were defined. Every FLAC file in the current folder will be\n" +
				"converted and the resulting MP3 files stored in the same folder.")


# Methods :: Command line options and instructions
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Help instructions for the application.
# *************************************************************************************************
def help():
	print "Usage: flactomp3 [-f] [filenames] [-d] [folder]"
	print "    -f\n        specify a set of files to convert"
	print "    -d\n        folder in which the generated MP3 files will be saved"
	print "    --help\n        display this help and exit"
	print "    --version\n        output version information and exit\n"


# *************************************************************************************************
# Current version of the application.
# *************************************************************************************************
def version():
	print "flactomp3 version 0.1.0\n"


# *************************************************************************************************
# Validates the input command line arguments.
#
# @param arguments List of command line arguments
# @return True if the program should continue its execution; False otherwise
# *************************************************************************************************
def check_arguments(arguments):

	# Checks if no options were set
	if len(arguments) == 1:
		version()
		help()
		return False

	# Checks if only one input argument is present
	elif len(arguments) == 2:

		# Checks if the argument is the help option
		if arguments[1] == OPTIONS["help"]:
			help()

		# Checks if the argument is the version option
		elif arguments[1] == OPTIONS["version"]:
			version()

		else:
			print ERROR_OPTION.format(arguments[1])

		return False

	# More than one input argument is present
	else:
		# Goes through the list of input arguments and looks for invalid options
		for arg in arguments:
			if arg.startswith("-") and arg not in OPTIONS.values():
				print ERROR_OPTION.format(arguments[1])
				return False

	return True


# *************************************************************************************************
# Validates the "-f" option that allows a user to specify a set of input FLAC files to convert.
#
# @param arguments List of command line arguments
# @return A list with the set of input FLAC files
# *************************************************************************************************
def some_files_option(arguments):

	# Goes through the list of input arguments and looks for invalid options
	for arg in arguments:
		if arg == OPTIONS["someFiles"]:
			index = arguments.index(arg) + 1
			if index == len(arguments):
				print ERROR_NO_FILES_GIVEN
				sys.exit()

			#for flac_file in arguments[index:]:



# *************************************************************************************************
# Validates the "-d" option that allows a user to specify a destination folder for the generated
# MP3 files.
#
# @param arguments List of command line arguments
# *************************************************************************************************
#def folder_option(arguments):

# Goes through the list of input arguments
	#for arg in arguments:
	#	if arg == OPTIONS["directory"]:
	#		for flac_file in arguments:


# Methods :: Folder and file library
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Checks if a folder contains, at least, one file.
#
# @param folder Folder to check for files
# @param suffix File suffix (e.g., check for specific file extensions)
# @return True if the folder contains any files; False otherwise
# *************************************************************************************************
def folder_has_files(folder, suffix=""):
	for item in os.listdir(folder):
		item_path = os.path.join(folder, item)
		if os.path.isfile(item_path) and item_path.suffix(suffix):
			return True

	print ERROR_NO_FILES.format(suffix)
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


# Methods :: Execution and boilerplate
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Defines the main workflow of the application
# *************************************************************************************************
def run():

	# Checks the input arguments
	if not check_arguments(sys.argv):
		sys.exit()

	# Checks if the current folder has any FLAC files
	if not folder_has_files(folder, EXT_FLAC):
		sys.exit()

	# Main workflow for the single FLAC file
	#tags = decode_flac(sys.argv[2])
	#encode_wav_flac(sys.argv[2], tags)
	#encode_wav_mp3(sys.argv[2], tags)


# *************************************************************************************************
# Main function
# *************************************************************************************************
def main():
	run()


# Standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()
