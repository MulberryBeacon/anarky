# -*- coding: utf-8 -*-
"""
Setup module.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# --------------------------------------------------------------------------------------------------
from setuptools import setup, find_packages

# Setup
# --------------------------------------------------------------------------------------------------
setup(
    name='anarky',
    version='0.0.1',
    description='A set of simple programs for encoding and decoding between several types of audio\
                 files.',
    author='Eduardo Ferreira',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['flac2mp3 = anarky.scripts.flac2mp3:run',
                            'flac2wav = anarky.scripts.flac2wav:run',
                            'wav2flac = anarky.scripts.wav2flac:run',
                            'wav2mp3 = anarky.scripts.wav2mp3:run'],
    }
)
