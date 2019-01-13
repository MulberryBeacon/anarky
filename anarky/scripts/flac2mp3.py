# -*- coding: utf8 -*-

"""
Encodes FLAC files into the MP3 format with the maximum compression level.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

from anarky.audio.encode import encode_flac_mp3
from anarky.enum.description import Description
from anarky.enum.script import Script
from anarky.interface import get_options

def run():
    (files, destination) = get_options(Script.FLAC2MP3.value, Description.FLAC2MP3.value, True)
    for item in files:
        encode_flac_mp3(item, destination)
