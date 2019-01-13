# -*- coding: utf8 -*-

"""
Utilities.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

from pathlib import Path

ENCODING = 'utf-8'


def is_string_empty(string: str) -> bool:
    """
    Checks if a string is empty.

    :param string:
        The string to check
    :return:
        True if the string is empty; False otherwise
    """
    return string is None or len(string) == 0


def update_extension(filename: str, extension: str = '') -> Path:
    """
    Updates the extension of the given file.
    If an extension is not provided, the extension from the given file is stripped.

    :param filename:
        The name of the file
    :param extension:
        The file extension
    :return:
        The name of the file updated with the given extension
    """
    return Path(filename).resolve().with_suffix(extension)


def update_path(filename: str, directory: str, extension: str = '') -> Path:
    """
    Updates the path and extension of the given file.
    If an extension is not provided, the extension from the given file is stripped.

    :param filename:
        The name of the file
    :param directory:
        The directory
    :param extension:
        The file extension
    :return:
        The name of the file updated with the given directory and extension
    """
    return Path(directory, Path(update_extension(filename, extension)).name).resolve()
