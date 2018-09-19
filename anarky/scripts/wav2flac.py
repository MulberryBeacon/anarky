# -*- coding: utf8 -*-

"""
Encodes WAV files into the FLAC format with the maximum compression level.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""
from anarky.audio.encode import encode_wav_flac
from anarky.enums.description import Description
from anarky.enums.script import Script
from anarky.library.general import keyboard_interrupt
from anarky.library.interface import get_options

def run():
    try:
        (files, destination) = get_options(Script.WAV2FLAC.value, Description.WAV2FLAC.value, True)

        output_files = []
        for item in files:
            output_file = encode_wav_flac(item, destination)
            if output_file:
                output_files.append(output_file[0])

    except KeyboardInterrupt:
        keyboard_interrupt()
