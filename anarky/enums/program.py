# -*- coding: utf8 -*-
"""
List of external programs used in the encoding and decoding operations.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

from enum import Enum

class Program(Enum):
    flac = 'flac'
    metaflac = 'metaflac'
    lame = 'lame'
    grep = 'grep'
    sed = 'sed'
    file = 'file'