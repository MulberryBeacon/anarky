# -*- coding: utf8 -*-
"""
List of audio file extensions.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

from enum import Enum

class AudioFile(Enum):
    flac = '.flac'
    mp3 = '.mp3'
    wav = '.wav'