#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Encodes FLAC files into the MP3 format with the maximum compression level.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# --------------------------------------------------------------------------------------------------
from anarky.library.audio import encode_flac_mp3
from anarky.library.general import keyboard_interrupt
from anarky.library.interface import get_options


# Constants
# --------------------------------------------------------------------------------------------------
PROGRAM = 'flac2mp3'
DESCRIPTION = 'Encodes FLAC files into the MP3 format with the maximum compression level'


# Methods :: Execution and boilerplate
# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        #(files, destination, cover, tags, playlist) = get_options(PROGRAM, DESCRIPTION, True)
        (files, destination) = get_options(PROGRAM, DESCRIPTION, True)

        output_files = []
        for item in files:
            #output_file = encode_flac_mp3(item, destination, cover, tags)
            output_file = encode_flac_mp3(item, destination)
            if output_file:
                output_files.append(output_file)

    except KeyboardInterrupt:
        keyboard_interrupt()
