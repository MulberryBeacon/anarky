# -*- coding: utf8 -*-

"""
Audio metadata management operations.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

from json import dump, load
from os.path import join
from subprocess import call, CalledProcessError, check_output, PIPE, Popen
import sys

from anarky.enum.program import Program
from anarky.utils import ENCODING, is_string_empty, update_extension, update_path


"""
TITLE       : Track/Work name
ARTIST      : The artist generally considered responsible for the work. In popular music this is
              usually the performing band or singer. For classical music it would be the composer.
              For an audio book it would be the author of the original text
ALBUM       : The collection name to which this track belongs
TRACKNUMBER : The track number of this piece if part of a specific larger collection or album
ALBUMARTIST : The artist(s) who performed the work. In classical music this would be the conductor,
              orchestra, soloists. In an audio book it would be the actor who did the reading. In
              popular music this is typically the same as the ARTIST and is omitted
GENRE       : A short text indication of music genre
DATE        : Date the track was recorded
DISCTOTAL   : Number of discs that compose the set
TRACKTOTAL  : Number of tracks in the album
"""
TAGS = {
    'TITLE': '--tt',
    'ARTIST': '--ta',
    'ALBUM': '--tl',
    'TRACKNUMBER': '--tn',
    'ALBUMARTIST': ['--tv', 'TPE2='],
    'GENRE': '--tg',
    'DATE': '--ty',
    'DISCTOTAL': ['--tv', 'TPOS='],
    'TRACKTOTAL': ''
}


def get_cover(filename: str, destination: str) -> str:
    """
    Retrieves the front cover art file from a FLAC audio file and stores it in the destination
    directory.

    :param filename:
        The input audio file name
    :param destination:
        The destination where the output file will be stored
    :return:
        The name of the album art file
    """
    # Prepares the 'metaflac' program arguments:
    # --list       => Lists the full stack of metadata
    # --block-type => Comma-separated list of block types to be included
    metaflac = [Program.METAFLAC.value, '--list', '--block-type=PICTURE', filename]

    # Prepares the 'grep' program arguments (looks for description parameter)
    grep = [Program.GREP.value, 'description:']

    # Prepares the 'sed' program arguments (the regular expression removes the parameter name)
    sed = [Program.SED.value, 's/.*: //']

    # Invokes the 'metaflac', 'grep' and 'sed' programs to retrieve the cover file name
    p1 = Popen(metaflac, stdout=PIPE)
    p2 = Popen(grep, stdin=p1.stdout, stdout=PIPE)
    p3 = Popen(sed, stdin=p2.stdout, stdout=PIPE)
    cover = p3.stdout.read().decode(ENCODING).rstrip('\n')
 
    # Checks if the audio file has a cover
    if is_string_empty(cover):
        return None

    # Prepares the 'metaflac' program arguments:
    # --export-picture-to => Export PICTURE block to a file
    cover = join(destination, cover)
    call([Program.METAFLAC.value, '--export-picture-to=' + cover, filename])

    return cover


def read_tags(filename: str) -> str:
    """
    Reads a JSON file with ID3 tags.

    :param filename:
        The input audio file name
    :return:
        The name of the ID3 tags file
    """
    try:
        with open(update_extension(filename, '.json'), 'r') as tags_file:
            tags = load(tags_file)
    except FileNotFoundError:
        return None

    return tags


def write_tags(filename: str, tags: list(str)):
    """
    Writes ID3 tags to a JSON file.

    :param filename:
        The input audio file name
    :param tags:
        The list of ID3 tags written to the audio file
    """
    with open(update_extension(filename, '.json'), 'w') as tags_file:
        dump(tags, tags_file, indent=4)


def get_tags(filename: str) -> list(str):
    """
    Retrieves the tag values of a FLAC audio file.

    :param filename:
        The input audio file name
    :return:
        The list of ID3 tags retrieved from the audio file
    """
    tags = {}
    for tag in TAGS:

        # Invokes the 'metaflac' program with the following arguments:
        # --show-tag => Shows the value of the given tag
        p = Popen([Program.METAFLAC.value, '--show-tag=' + tag, filename], stdout=PIPE)
        value = p.stdout.read().decode(ENCODING).rstrip('\n')
        if value:
            tags[tag] = value.split('=')[1]

    return tags
