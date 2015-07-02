#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Encodes FLAC files into the MP3 format with the maximum compression level.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# -------------------------------------------------------------------------------------------------
from audio import encode_flac_mp3#, read_tag_file
from general import file_strip_full
from interface import get_options

# Constants
# -------------------------------------------------------------------------------------------------
PROGRAM = 'flac2mp3'
DESCRIPTION = 'Encodes FLAC files into the MP3 format with the maximum compression level'

# Methods :: Execution and boilerplate
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        (files, destination, cover, tags, playlist) = get_options(PROGRAM, DESCRIPTION)
        for item in files:
            encode_flac_mp3(item, destination, cover, tags)

        # if playlist:
        #     from audio import create_playlist
        #     create_playlist(destination, "artist", "album")

    except KeyboardInterrupt:
        from general import ERROR_INTERRUPTED
        print('\n', ERROR_INTERRUPTED, '\n')
