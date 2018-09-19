# -*- coding: utf8 -*-

"""
Decodes FLAC files into the WAV format.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""
from anarky.audio.decode import decode_flac_wav
from anarky.enums.description import Description
from anarky.enums.script import Script
from anarky.library.general import keyboard_interrupt
from anarky.library.interface import get_options

def run():
    try:
        (files, destination) = get_options(Script.FLAC2WAV.value, Description.FLAC2WAV.value, True)

        output_files = []
        for item in files:
            output_file = decode_flac_wav(item, destination)
            if output_file:
                output_files.append(output_file[0])

    except KeyboardInterrupt:
        keyboard_interrupt()
