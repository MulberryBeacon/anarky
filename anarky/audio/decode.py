# -*- coding: utf8 -*-

"""
Audio decoding operations.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

from subprocess import call
import logging

from anarky.enum.program import Program
from anarky.enum.audio_file import AudioFile
from anarky.library.general import update_path
from anarky.miscellaneous.external import is_program_available

# Logger
# --------------------------------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

# Methods
# --------------------------------------------------------------------------------------------------
def decode_flac_wav(filename: str, destination: str) -> str:
    """
    Decodes a FLAC audio file, generating the corresponding WAV audio file.

    :param filename:
        The input audio file name
    :param destination:
        The destination where the output file will be stored
    :return:
        The output audio file name
    """
    is_program_available(Program.FLAC.value)

    if not is_flac_file(filename):
        return None

    # Invokes the 'flac' program with the following arguments:
    # -d => Decode (the default behavior is to encode)
    # -f => Force overwriting of output files
    # -o => Force the output file name
    output_filename = update_path(filename, destination, AudioFile.WAV.value)
    call([Program.FLAC.value, '-df', filename, '-o', output_filename])

    return output_filename
