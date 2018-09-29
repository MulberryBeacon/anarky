# -*- coding: utf8 -*-

"""
Audio decoding operations.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

from subprocess import call

from anarky.enum.program import Program
from anarky.enum.audio_file import AudioFile
from anarky.utils import update_path


def decode_flac_wav(filename: str, destination: str) -> str:
    """
    Decodes a FLAC audio file, generating the corresponding WAV audio file.
    
    The 'flac' program is executed with the following arguments:
      * -d => Decode (the default behavior is to encode)
      * -f => Force overwriting of output files
      * -o => Force the output file name

    :param filename:
        The input audio file name
    :param destination:
        The destination where the output file will be stored
    :return:
        The output audio file name
    """
    output_filename = update_path(filename, destination, AudioFile.WAV.value)
    call([Program.FLAC.value, '-df', filename, '-o', output_filename])

    return output_filename
