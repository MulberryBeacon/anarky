# -*- coding: utf8 -*-

"""
Encodes FLAC files into the MP3 format with the maximum compression level.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""
from anarky.audio.encode import encode_flac_mp3
from anarky.enums.description import Description
from anarky.enums.script import Script
from anarky.library.general import keyboard_interrupt
from anarky.library.interface import get_options

def run():
    try:
        (files, destination) = get_options(Script.FLAC2MP3.value, Description.FLAC2MP3.value, True)

        output_files = []
        for item in files:
            output_file = encode_flac_mp3(item, destination)
            if output_file:
                output_files.append(output_file)

    except KeyboardInterrupt:
        keyboard_interrupt()
