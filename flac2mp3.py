#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Encodes FLAC files into the MP3 format with the maximum compression level.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# -------------------------------------------------------------------------------------------------
from audio import EXTENSIONS, encode_flac_mp3
from interface import parse_options

# Constants
# -------------------------------------------------------------------------------------------------
PROGRAM = "flac2mp3"
DESCRIPTION = "Encodes FLAC files into the MP3 format with the maximum compression level"

# Methods :: Execution and boilerplate
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	try:
		(files, destination, cover, tags, playlist) = parse_options(PROGRAM, DESCRIPTION, EXTENSIONS["flac"])
		for item in files:
			encode_flac_mp3(item, destination, cover, (tags[item] if tags else tags))

		if playlist:
			from audio import create_playlist
			create_playlist(destination, "artist", "album")

	except KeyboardInterrupt:
		from interface import ERROR_INTERRUPTED
		print "\n" + ERROR_INTERRUPTED + "\n"
