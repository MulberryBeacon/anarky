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
def decode_flac_wav(filename: str, destination: str, extract_cover: bool = False, extract_tags: bool = False) -> str:
    """
    Decodes a FLAC audio file, generating the corresponding WAV audio file.
    Also retrieves its ID3 tags and album cover.

    :param filename:
        The input audio file name
    :param destination:
        The destination where the output file will be stored
    :param extract_cover:
        Indicates if the album art should be extracted from the audio file
    :param extract_tags:
        Indicates if the ID3 tags should be extracted from the audio file
    :return:
        A tuple with three file names: output audio file, album art file and ID3 tags file
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

    # Checks if both cover and tags should be retrieved
    #cover = get_cover(filename, destination) if extract_cover else None
    #tags = get_tags(filename) if extract_tags else None

    #return output_filename, cover, tags
    return output_filename
