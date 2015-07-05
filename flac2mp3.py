#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Encodes FLAC files into the MP3 format with the maximum compression level.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# -------------------------------------------------------------------------------------------------
from audio import encode_flac_mp3
from general import keyboard_interrupt
from interface import get_options

# Constants
# -------------------------------------------------------------------------------------------------
PROGRAM = 'flac2mp3'
DESCRIPTION = 'Encodes FLAC files into the MP3 format with the maximum compression level'

# Methods :: Execution and boilerplate
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        (files, destination, cover, tags, playlist) = get_options(PROGRAM, DESCRIPTION, True)

        output_files = []
        for item in files:
            output_file = encode_flac_mp3(item, destination, cover, tags)
            if output_file:
                output_files.append(output_file)

        if playlist:
            from audio import create_playlist
            create_playlist(output_files, destination)

    except KeyboardInterrupt:
        keyboard_interrupt()
