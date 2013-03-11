#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Encodes WAV files into the FLAC format with the maximum compression level.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import section
# -------------------------------------------------------------------------------------------------
from audio import encode_wav_flac
from interface import check_options
import sys

# Methods :: Execution and boilerplate
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	try:
		(files, destination, cover, tags, playlist) = check_options(sys.argv)
		for item in files:
			encode_wav_flac(item, destination, cover, (tags[item] if tags else tags))

		if playlist:
			from audio import create_playlist
			create_playlist(destination, "artist", "album")

	except KeyboardInterrupt:
		from interface import ERROR_INTERRUPTED
		print "\n" + ERROR_INTERRUPTED + "\n"
