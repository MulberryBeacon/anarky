#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Decodes FLAC files into the WAV format.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# -------------------------------------------------------------------------------------------------
from audio import EXTENSIONS, decode_flac_wav
from interface import parse_options

# Constants
# -------------------------------------------------------------------------------------------------
PROGRAM = "flac2wav"
DESCRIPTION = "Decodes FLAC files into the WAV format"

# Methods :: Execution and boilerplate
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	try:
		(files, destination, cover, tags) = parse_options(PROGRAM, DESCRIPTION, EXTENSIONS["flac"], True)
		for item in files:
			decode_flac_wav(item, destination, cover, tags)

	except KeyboardInterrupt:
		from general import ERROR_INTERRUPTED
		print "\n" + ERROR_INTERRUPTED + "\n"
