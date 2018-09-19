# -*- coding: utf8 -*-

"""
Encodes WAV files into the FLAC format with the maximum compression level.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""
from anarky.audio.encode import encode_wav_flac
from anarky.enum.description import Description
from anarky.enum.script import Script
from anarky.library.general import keyboard_interrupt
from anarky.library.interface import get_options

def run():
    try:
        (files, destination) = get_options(Script.WAV2FLAC.value, Description.WAV2FLAC.value, True)
        for item in files:
            encode_wav_flac(item, destination)

    except KeyboardInterrupt:
        keyboard_interrupt()
