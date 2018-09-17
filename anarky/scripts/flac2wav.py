# -*- coding: utf8 -*-
"""
Decodes FLAC files into the WAV format.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# --------------------------------------------------------------------------------------------------
from anarky.audio.decode import decode_flac_wav
from anarky.library.audio import write_tags
from anarky.library.general import keyboard_interrupt
from anarky.library.interface import get_options


# Constants
# --------------------------------------------------------------------------------------------------
PROGRAM = 'flac2wav'
DESCRIPTION = 'Decodes FLAC files into the WAV format'


# Methods :: Execution
# --------------------------------------------------------------------------------------------------
def run():
    try:
        #(files, destination, cover, tags, playlist) = get_options(PROGRAM, DESCRIPTION, True)
        (files, destination) = get_options(PROGRAM, DESCRIPTION, True)

        output_files = []
        for item in files:
            #output_file = decode_flac_wav(item, destination, cover, tags)
            output_file = decode_flac_wav(item, destination)
            if output_file:
                output_files.append(output_file[0])

    except KeyboardInterrupt:
        keyboard_interrupt()
