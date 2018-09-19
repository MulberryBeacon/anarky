# -*- coding: utf8 -*-

"""
List of external programs used in the encoding and decoding operations.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""
from enum import Enum

class Program(Enum):
    FLAC = 'flac'
    METAFLAC = 'metaflac'
    LAME = 'lame'
    GREP = 'grep'
    SED = 'sed'
    FILE = 'file'
    WHEREIS = 'whereis'
