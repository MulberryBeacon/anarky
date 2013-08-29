#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Encodes WAV files into the MP3 format with the maximum compression level.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# -------------------------------------------------------------------------------------------------
from audio import EXTENSIONS, encode_wav_mp3, read_tag_file
from general import file_strip_full
from interface import parse_options

# Constants
# -------------------------------------------------------------------------------------------------
PROGRAM = "wav2mp3"
DESCRIPTION = "Encodes WAV files into the MP3 format with the maximum compression level"

# Methods :: Execution and boilerplate
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	try:
		(files, destination, cover, tags, playlist) = parse_options(PROGRAM, DESCRIPTION, EXTENSIONS["wav"])
		map_tags = read_tag_file(tags) if tags else None
		for item in files:
			encode_wav_mp3(item, destination, cover, (map_tags[file_strip_full(item)] if tags else None))

		if playlist:
			from audio import create_playlist
			create_playlist(destination, map_tags, EXTENSIONS["mp3"])

	except KeyboardInterrupt:
		from general import ERROR_INTERRUPTED
		print "\n" + ERROR_INTERRUPTED + "\n"
