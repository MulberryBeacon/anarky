#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Decodes FLAC files into the WAV format.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# -------------------------------------------------------------------------------------------------
from audio import decode_flac_wav, write_tags
from general import keyboard_interrupt
from interface import get_options

# Constants
# -------------------------------------------------------------------------------------------------
PROGRAM = 'flac2wav'
DESCRIPTION = 'Decodes FLAC files into the WAV format'

# Methods :: Execution and boilerplate
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        (files, destination, cover, tags, playlist) = get_options(PROGRAM, DESCRIPTION, True)

        output_files = []
        for item in files:
            output_file = decode_flac_wav(item, destination, cover, tags)
            if output_file:
                output_files.append(output_file[0])
                write_tags(output_file[0], output_file[2])

        if playlist:
            from audio import create_playlist
            create_playlist(output_files, destination)

    except KeyboardInterrupt:
        keyboard_interrupt()
