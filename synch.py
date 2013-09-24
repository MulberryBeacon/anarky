#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Synchronization library.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# ----------------------------------------------------------------------------------------------------------------------
from audio import EXTENSIONS, decode_flac_wav, encode_wav_mp3
from os import listdir, makedirs
from os.path import abspath, isdir, isfile, join

import sys
#import collections
#import errno
#import re
#import subprocess


# Methods :: 
# ----------------------------------------------------------------------------------------------------------------------
def get_subdirs(root, prefix=""):
	"""
	Recursively navigates through a directory and returns the list of subdirectories.
	"""
	dirs = []
	for item in listdir(root):
		item_path = join(root, item)
		item_tree = join(prefix, item)
		if isdir(item_path):
			dirs.append(item_tree)
			dirs.extend(get_subdirs(item_path, item_tree))

	return dirs

"""
def get_files(directory, extension):
	
	Retrieves the list of files in a directory that have the given extension and adds their full path.
	
	flac_list = [join(directory, item) for item in listdir(directory) if item.endswith(extension)]
	return [flac_file for flac_file in flac_list if isfile(flac_file)]
"""

def get_files(directory):
	"""
	Retrieves the list of files in a directory and adds their full path.
	"""
	entry_list = [join(directory, item) for item in listdir(directory)]
	return [item for item in entry_list if isfile(item)]


def does_stuff(dir_flac, dir_mp3):
	"""
	1) Check top level folders with artist names
	2) If it exists, move to the subfolders and create any missing albums
	3) If it doesn't exist, create the artist folder and the corresponding subfolders with albums

	2) folder with FLAC files => encode the list of files
	3) folder has subfolders => indicates a multi CD album
	"""
	# Stores the full path of both FLAC and MP3 directories
	root_flac = abspath(dir_flac)
	root_mp3 = abspath(dir_mp3)

	# Retrieves the list of subdirectories of both FLAC and MP3 directories
	subdirs_flac = get_subdirs(root_flac)
	subdirs_mp3 = get_subdirs(root_mp3)

	# Goes through the list of missing directories
	missing_dirs = [diff for diff in subdirs_flac if not diff in subdirs_mp3]
	print subdirs_flac, len(subdirs_flac)
	print subdirs_mp3, len(subdirs_mp3)
	print missing_dirs, len(missing_dirs)
	print '====================================================='
	for missing_dir in missing_dirs:

		# Sets the full path for the source and destination directories
		source_dir = join(root_flac, missing_dir)
		destination_dir = join(root_mp3, missing_dir)

		# Creates the new directory in the MP3 folder
		try:
			makedirs(destination_dir)
		except OSError, e:
			if e.errno != errno.EEXIST:
				raise

		"""
		# Case #1: check if the source directory has any FLAC files to encode
		list_files = get_files(source_dir, EXTENSIONS["flac"])
		if len(list_files) == 0:
			print "[INFO] No FLAC files to process!"

		# Case #2: check if the source directory has any WAV files to encode
		list_files = get_files(source_dir, EXTENSIONS["wav"])
		if len(list_files) == 0:
			print "[INFO] No WAV files to process!"
		"""
		list_files = get_files(source_dir)
		for item in list_files:

			# Case #1: check if the current entry is a FLAC file
			if item.endswith(EXTENSIONS["flac"]):
				(wav_filename, cover_filename, tags_value) = decode_flac_wav(flac, source_dir, True, True)

				# Checks any ID3 tags were retrieved
				if not tags_value:
					# apply yet to be implemented mechanism to retrieve the necessary information for ID3 tags from the file structure
					print "[INFO] No tags!"

				encode_wav_flac(item, destination_dir, None, tags_value)
				encode_wav_mp3(wav_filename, destination_dir, None, tags_value)

			# Case #2: check if the current entry is a WAV file
			if item.endswith(EXTENSIONS["wav"]):
				# tags_value = apply yet to be implemented mechanism to retrieve the necessary information for ID3 tags from the file structure
				encode_wav_flac(item, destination_dir, None, tags_value)
				encode_wav_mp3(item, destination_dir, None, tags_value)


# Methods :: Execution and boilerplate
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	does_stuff(sys.argv[1], sys.argv[2])
