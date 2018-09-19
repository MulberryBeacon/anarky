# -*- coding: utf8 -*-

"""
List of descriptions for the scripts provided by Anarky.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""
from enum import Enum

class Description(Enum):
    FLAC2WAV = 'Decodes FLAC files into the WAV format'
    FLAC2MP3 = 'Encodes FLAC files into the MP3 format with the maximum compression level'
    WAV2FLAC = 'Encodes WAV files into the FLAC format with the maximum compression level'
    WAV2MP3 = 'Encodes WAV files into the MP3 format with the maximum compression level'
