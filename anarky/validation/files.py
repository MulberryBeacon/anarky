# -*- coding: utf8 -*-

"""
Operations to validate external dependencies.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""
from subprocess import call, PIPE, Popen
import logging
import sys

from anarky.enum.program import Program


logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def is_flac_file(filename):
    """
    Checks if the given file is a valid FLAC audio file.
    :param filename: The input audio file name
    :return: True if the input file is a FLAC audio file; False otherwise
    """
    is_program_available(Programs.metaflac.value)

    # Invokes the 'metaflac' program with the following arguments:
    # --show-md5sum => Show the MD5 signature from the STREAMINFO block
    output = ''
    try:
        output = check_output([Programs.metaflac.value, '--show-md5sum', filename]).decode(ENCODING)
    except CalledProcessError as e:
        if e.returncode == 1:
            return False

    return match(r'[a-z0-9]+', output)


def is_wav_file(filename):
    """
    Checks if the given file is a valid WAV audio file.
    :param filename: The input audio file name
    :return: True if the input file is a WAV audio file; False otherwise
    """
    is_program_available(Programs.file.value)

    # Invokes the 'file' program with the following arguments:
    # --mime-type => Output the MIME type
    output = ''
    try:
        output = check_output([Programs.file.value, '--mime-type', filename]).decode(ENCODING)
    except CalledProcessError as e:
        if e.returncode == 1:
            return False

    return 'audio/x-wav' in output
