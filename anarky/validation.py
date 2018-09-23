# -*- coding: utf8 -*-

"""
Validation of external dependencies and file types.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

from subprocess import call, CalledProcessError, check_output, PIPE, Popen
from re import match
import logging
import sys

from anarky.enum.program import Program
from anarky.utils import ENCODING


logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def is_program_available(program: str) -> bool:
    """
    Checks if an external program is present in the operating system.

    :param program:
        The name of the external program
    :return:
        True if the program is present in the operating system; False otherwise
    """
    # The output of the following command should be something like:
    # flac: /usr/bin/flac /usr/share/man/man1/flac.1.gz
    output = Popen([Program.WHEREIS.value, program], stdout=PIPE).communicate()[0]
    if len(output.split()) == 1:
        _logger.error('Program \'{}\' was not found!'.format(program))
        sys.exit(1)
    # TODO: needs to return a boolean


def is_flac_file(filename: str) -> bool:
    """
    Checks if the given file is a valid FLAC audio file.

    The 'metaflac' program is executed with the following arguments:
      * --show-md5sum => Show the MD5 signature from the STREAMINFO block

    :param filename:
        The input audio file name
    :return:
        True if the input file is a FLAC audio file; False otherwise
    """
    output = ''
    try:
        output = check_output([Program.METAFLAC.value, '--show-md5sum', filename]).decode(ENCODING)
    except CalledProcessError as e:
        if e.returncode == 1:
            return False

    return match(r'[a-z0-9]+', output)


def is_wav_file(filename: str) -> bool:
    """
    Checks if the given file is a valid WAV audio file.

    The 'file' program is executed with the following arguments:
      * --mime-type => Output the MIME type

    :param filename:
        The input audio file name
    :return:
        True if the input file is a WAV audio file; False otherwise
    """
    output = ''
    try:
        output = check_output([Program.FILE.value, '--mime-type', filename]).decode(ENCODING)
    except CalledProcessError as e:
        if e.returncode == 1:
            return False

    return 'audio/x-wav' in output
