# -*- coding: utf8 -*-

"""
Decodes FLAC files into the WAV format.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

from anarky.audio.decode import decode_flac_wav
from anarky.enum.description import Description
from anarky.enum.script import Script
from anarky.utils import keyboard_interrupt
from anarky.interface import get_options

def run():
    try:
        (files, destination) = get_options(Script.FLAC2WAV.value, Description.FLAC2WAV.value, True)
        for item in files:
            decode_flac_wav(item, destination)

    except KeyboardInterrupt:
        keyboard_interrupt()
