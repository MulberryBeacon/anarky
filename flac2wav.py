#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Decodes FLAC files into the WAV format.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import section
# -------------------------------------------------------------------------------------------------
from audio import EXTENSIONS, decode_flac_wav
from interface import check_options

# Module import section
# -------------------------------------------------------------------------------------------------
PROGRAM = "flac2wav"
DESCRIPTION = "Decodes FLAC files into the WAV format"

# Methods :: Execution and boilerplate
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	try:
		(files, destination, cover, tags, playlist) = check_options(PROGRAM, DESCRIPTION, EXTENSIONS["flac"])
		for item in files:
			decode_flac_wav(item, destination, cover, tags)

		if playlist:
			from audio import create_playlist
			create_playlist(destination, "artist", "album")

	except KeyboardInterrupt:
		from interface import ERROR_INTERRUPTED
		print "\n" + ERROR_INTERRUPTED + "\n"
