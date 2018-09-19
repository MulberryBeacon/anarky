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
