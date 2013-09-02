#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Synchronization library.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# ----------------------------------------------------------------------------------------------------------------------
from audio import EXTENSIONS
from os import listdir, makedirs
from os.path import abspath, isdir, isfile, join

import sys
#import collections
#import errno
#import re
#import subprocess


# Methods :: 
# ----------------------------------------------------------------------------------------------------------------------
def get_subfolders(root, prefix=""):
	"""
	Recursively navigates through a folder and returns the list of subfolders.
	"""
	folders = []
	for item in listdir(root):
		item_path = join(root, item)
		item_tree = join(prefix, item)
		if isdir(item_path):
			folders.append(item_tree)
			folders.extend(get_subfolders(item_path, item_tree))

	return folders


def folder_has_files(folder):
	"""
	Checks if a folder contains, at least, one file.
	"""
	for item in os.listdir(folder):
		item_path = os.path.join(folder, item)
		if isfile(item_path) and item_path.endswith(EXTENSIONS["flac"]):
			return True

	return False


def does_stuff(folder_flac, folder_mp3):
	"""
	1) Check top level folders with artist names
	2) If it exists, move to the subfolders and create any missing albums
	3) If it doesn't exist, create the artist folder and the corresponding subfolders with albums
	"""
	# Stores the full path of both FLAC and MP3 folders
	root_flac = abspath(folder_flac)
	root_mp3 = abspath(folder_mp3)
	print root_flac
	print root_mp3

	# Retrieves the list of subfolders of both FLAC and MP3 folders
	folders_flac = get_subfolders(root_flac)
	folders_mp3 = get_subfolders(root_mp3)
	print folders_flac, len(folders_flac)
	print folders_mp3, len(folders_mp3)

	matches = [folder for folder in folders_flac if not folder in folders_mp3]
	print matches, len(matches)
	for match in matches:

		# Creates a new folder
		try:
			makedirs(join(root_mp3, match))
		except OSError, e:
			if e.errno != errno.EEXIST:
				raise

		# Checks if the folder has any FLAC files to encode
		source_folder = join(root_flac, match)
		if not folder_has_files(source_folder):
			print "[ERROR] Fudge it!"
			continue

		

		# Possible cases:
		# 1) folder without any FLAC files => [ERROR]
		# 2) folder with FLAC files => encode the list of files
		# 3) folder has subfolders => indicates a multi CD album

		# Checks if folder has any files to convert
		#if folder_has_files(join(root_flac, match)):
			


# Methods :: Execution and boilerplate
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	does_stuff(sys.argv[1], sys.argv[2])
