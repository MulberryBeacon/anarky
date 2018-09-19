# -*- coding: utf8 -*-

"""
Encodes WAV files into the MP3 format with the maximum compression level.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""
from anarky.audio.encode import encode_wav_mp3
from anarky.enum.description import Description
from anarky.enum.script import Script
from anarky.library.general import keyboard_interrupt
from anarky.library.interface import get_options

def run():
    try:
        (files, destination) = get_options(Script.WAV2MP3.value, Description.WAV2MP3.value, True)

        output_files = []
        for item in files:
            output_file = encode_wav_mp3(item, destination)
            if output_file:
                output_files.append(output_file[0])

    except KeyboardInterrupt:
        keyboard_interrupt()
