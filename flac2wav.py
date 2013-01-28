#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Decodes FLAC files into the WAV format.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import section
# -------------------------------------------------------------------------------------------------
from audio import encode_wav_flac, set_cover, EXTENSIONS
from miscellaneous import indent
import interface as cli
import os
import sys


# Constants :: Information messages
# -------------------------------------------------------------------------------------------------
ERROR_INTERRUPTED = "The program execution was interrupted!"

INFO_HELP = ("Usage: flac2wav [OPTION] [input-files] [-d] [destination]\n\n" +
			"OPTIONS:\n" +
			indent(1) + "-f\n" + indent(2) + "specify a set of files to convert\n" +
			indent(1) + "-F\n" + indent(2) + "folder with a set of files to convert\n" +
			indent(1) + "-d\n" + indent(2) + "folder in which the generated WAV files will be saved\n" +
			indent(1) + "-h\n" + indent(2) + "display this help and exit\n" +
			indent(1) + "-v\n" + indent(2) + "output version information and exit\n")

INFO_VERSION = "flac2wav version 0.0.1\n"


# Methods :: Execution and boilerplate
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Defines the main workflow of the application.
#
# @param arguments Command line arguments
# *************************************************************************************************
def run(arguments):

	# Checks the set of information options
	if (not cli.check_option_none(arguments, INFO_VERSION, INFO_HELP)
		or not cli.check_option_version(arguments, INFO_VERSION)
		or not cli.check_option_help(arguments, INFO_HELP)):
		sys.exit()

	# Default values for the source file list and destination folder
	files = []
	destination = os.getcwd()

	# Pre-processes the option list
	options = cli.split_options(arguments)
	source_flag = False

	# Goes through the list of options
	for option, values in options.items():

		# Option "-d"
		if option == cli.OPTIONS["directory"]:
			destination = cli.check_option_folder(values)
			if destination == None:
				sys.exit()
		else:
			# Option "-f"
			if option == cli.OPTIONS["somefiles"]:
				file_list = cli.check_option_somefiles(values, EXTENSIONS["flac"])

			# Option "-F"
			elif option == cli.OPTIONS["allfiles"]:
				file_list = cli.check_option_allfiles(values, EXTENSIONS["flac"])

			if file_list == None:
				sys.exit()

			files.extend(file_list)
			source_flag = True

	# Checks if any FLAC files were given
	if not source_flag:
		print ERROR_NO_FILES_GIVEN.format(EXTENSIONS["flac"])
		sys.exit()

	# Runs the main workflow for each FLAC file
	for item in files:
		decode_flac_wav(item, destination)


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
