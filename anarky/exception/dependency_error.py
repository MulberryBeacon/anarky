# -*- coding: utf8 -*-
"""
Exception used when validating external dependencies.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""
class DependencyError(Exception):
    def __init__(self, program):
        return 'Program \'{}\' was not found!'.format(program)
