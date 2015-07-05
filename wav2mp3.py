#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Encodes WAV files into the MP3 format with the maximum compression level.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# -------------------------------------------------------------------------------------------------
from audio import encode_wav_mp3, read_tags
from general import WARNING_NO_JSON_FILE, keyboard_interrupt
from interface import get_options

# Constants
# -------------------------------------------------------------------------------------------------
PROGRAM = 'wav2mp3'
DESCRIPTION = 'Encodes WAV files into the MP3 format with the maximum compression level'

# Methods :: Execution and boilerplate
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        (files, destination, cover, tags, playlist) = get_options(PROGRAM, DESCRIPTION)

        output_files = []
        for item in files:
            file_tags = read_tags(item) if tags else None
            if tags and not file_tags:
                print(WARNING_NO_JSON_FILE)

            output_file = encode_wav_mp3(item, destination, cover, file_tags)
            if output_file:
                output_files.append(output_file[0])

        if playlist:
            from audio import create_playlist
            create_playlist(output_files, destination)

    except KeyboardInterrupt:
        keyboard_interrupt()
