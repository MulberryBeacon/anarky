# -*- coding: utf8 -*-

"""
List of audio file extensions.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

from enum import Enum

class AudioFile(Enum):
    """
    Audio file types.
    """
    FLAC = '.flac'
    MP3 = '.mp3'
    WAV = '.wav'
