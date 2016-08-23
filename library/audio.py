#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Audio library with conversion methods.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import
# --------------------------------------------------------------------------------------------------
from general import is_string_empty, update_extension, update_path

from enum import Enum
from json import dump, load
from os.path import basename, join
from re import match
from subprocess import call, CalledProcessError, check_output, PIPE, Popen
import logging
import sys


# Logger
# --------------------------------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


# Constants :: Error messages
# --------------------------------------------------------------------------------------------------
ERROR_PROGRAM_NOT_FOUND = 'Program \'{}\' was not found!'


# Constants :: Lists and file extensions
# --------------------------------------------------------------------------------------------------
ENCODING = 'utf-8'

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


# Classes
# --------------------------------------------------------------------------------------------------
# Represents audio file extensions
class AudioFile(Enum):
    flac = '.flac'
    mp3 = '.mp3'
    wav = '.wav'


# Represents external programs used in the encoding and decoding operations
class Programs(Enum):
    flac = 'flac'
    metaflac = 'metaflac'
    lame = 'lame'
    grep = 'grep'
    sed = 'sed'
    file = 'file'


# Methods :: File encoding and decoding
# --------------------------------------------------------------------------------------------------
def decode_flac_wav(filename, destination, extract_cover=False, extract_tags=False):
    """
    Decodes a FLAC audio file, generating the corresponding WAV audio file.
    Also retrieves its ID3 tags and album cover.
    :param filename: The input audio file name
    :param destination: The destination where the output file will be stored
    :param extract_cover: Indicates if the album art should be extracted from the audio file
    :param extract_tags: Indicates if the ID3 tags should be extracted from the audio file
    :return: A tuple with three file names: output audio file, album art file and ID3 tags file
    """
    is_program_available(Programs.flac.value)

    if not is_flac_file(filename):
        return None

    # Invokes the 'flac' program with the following arguments:
    # -d => Decode (the default behavior is to encode)
    # -f => Force overwriting of output files
    # -o => Force the output file name
    output_filename = update_path(filename, destination, AudioFile.wav.value)
    call([Programs.flac.value, '-df', filename, '-o', output_filename])

    # Checks if both cover and tags should be retrieved
    cover = get_cover(filename, destination) if extract_cover else None
    tags = get_tags(filename) if extract_tags else None

    return output_filename, cover, tags


def encode_wav_flac(filename, destination, cover=None, tags=None):
    """
    Encodes a WAV audio file, generating the corresponding FLAC audio file.
    :param filename: The input audio file name
    :param destination: The destination where the output file will be stored
    :param cover: The name of the file with the album art
    :param tags: The name of the file with the ID3 tags
    :return: The name of the output audio file
    """
    is_program_available(Programs.flac.value)

    if not is_wav_file(filename):
        return None

    # Prepares the 'flac' program arguments:
    # -f => Force overwriting of output files
    # -8 => Synonymous with -l 12 -b 4096 -m -e -r 6
    # -V => Verify a correct encoding
    # -o => Force the output file name
    output_filename = update_path(filename, destination, AudioFile.flac.value)
    flac = [Programs.flac.value, '-f8V', '-o', output_filename]

    # Prepares the cover file to be passed as a parameter
    # --picture=SPECIFICATION => Import picture and store in PICTURE block
    if cover:
        flac.extend(['--picture=3||' + basename(cover) + '||' + cover])

    # Prepares the FLAC tags to be passed as parameters
    # --T FIELD=VALUE => Add a FLAC tag; may appear multiple times
    if tags:
        for tag, value in tags.items():
            flac.extend(['-T', tag + '=' + value])

    # Invokes the 'flac' program
    flac.append(filename)
    call(flac)

    return output_filename


def encode_wav_mp3(filename, destination, cover=None, tags=None):
    """
    Encodes a WAV audio file, generating the corresponding MP3 audio file.
    :param filename: The input audio file name
    :param destination: The destination where the output file will be stored
    :param cover: The name of the file with the album art
    :param tags: The name of the file with the ID3 tags
    :return: The name of the output audio file
    """
    is_program_available(Programs.lame.value)

    if not is_wav_file(filename):
        return None

    # Prepares the 'lame' program arguments:
    # -b 320          => Set the bitrate to 320 kbps
    # -q 0            => Highest quality, very slow
    # --preset insane => Type of the quality settings
    # --id3v2-only    => Add only a version 2 tag
    output_filename = update_path(filename, destination, AudioFile.mp3.value)
    lame = [Programs.lame.value, '-b', '320', '-q', '0', '--preset', 'insane', '--id3v2-only']

    # Prepares the cover file to be passed as a parameter
    # --ti <file> => Audio/song albumArt (jpeg/png/gif file, v2.3 tag)
    if cover:
        lame.extend(['--ti', cover])

    # Prepares the ID3 tags to be passed as parameters
    # --<tag> <value> => Audio/song specific information
    if tags:
        for tag, value in tags.items():
            id3_tag = TAGS[tag]
            if not id3_tag:
                continue

            if tag == 'TRACKNUMBER':
                value += '/' + tags['TRACKTOTAL']

            lame.extend([id3_tag, value]
                if type(id3_tag) is not list
                else [id3_tag[0], id3_tag[1] + value])

    # Invokes the 'lame' program
    lame.extend([filename, output_filename])
    call(lame)

    return output_filename


def encode_flac_mp3(filename, destination, extract_cover=False, extract_tags=False):
    """
    Decodes a FLAC audio file, generating the corresponding WAV audio file.
    The WAV audio file is then encoded, generating the corresponding MP3 audio file.
    :param filename: The input audio file name
    :param destination: The destination where the output file will be stored
    :param extract_cover: Indicates if the album art should be extracted from the audio file
    :param extract_tags: Indicates if the ID3 tags should be extracted from the audio file
    :return: The name of the output audio file
    """
    wav_file = decode_flac_wav(filename, destination, extract_cover, extract_tags)
    if wav_file:
        cover = wav_file[1] if get_cover else None
        tags = wav_file[2] if get_tags else None
        return encode_wav_mp3(wav_file[0], destination, cover, tags)

    return None


# Methods :: Album cover management
# --------------------------------------------------------------------------------------------------
def get_cover(filename, destination):
    """
    Retrieves the front cover art file from a FLAC audio file and stores it in the destination
    directory.
    :param filename: The input audio file name
    :param destination: The destination where the output file will be stored
    ;return: The name of the album art file
    """
    is_program_available(Programs.metaflac.value)
    is_program_available(Programs.grep.value)
    is_program_available(Programs.sed.value)

    # Prepares the 'metaflac' program arguments:
    # --list       => Lists the full stack of metadata
    # --block-type => Comma-separated list of block types to be included
    metaflac = [Programs.metaflac.value, '--list', '--block-type=PICTURE', filename]

    # Prepares the 'grep' program arguments (looks for description parameter)
    grep = [Programs.grep.value, 'description:']

    # Prepares the 'sed' program arguments (the regular expression removes the parameter name)
    sed = [Programs.sed.value, 's/.*: //']

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
    call([Programs.metaflac.value, '--export-picture-to=' + cover, filename])

    return cover


# Methods :: Tag management
# --------------------------------------------------------------------------------------------------
def read_tags(filename):
    """
    Reads a JSON file with ID3 tags.
    :param filename: The input audio file name
    :return: The name of the ID3 tags file
    """
    try:
        with open(update_extension(filename, '.json'), 'r') as tags_file:
            tags = load(tags_file)
    except FileNotFoundError:
        return None

    return tags


def write_tags(filename, tags):
    """
    Writes ID3 tags to a JSON file.
    :param filename: The input audio file name
    :param tags: The list of ID3 tags written to the audio file
    """
    with open(update_extension(filename, '.json'), 'w') as tags_file:
        dump(tags, tags_file, indent=4)


def get_tags(filename):
    """
    Retrieves the tag values of a FLAC audio file.
    :param filename: The input audio file name
    :return: The list of ID3 tags retrieved from the audio file
    """
    is_program_available(Programs.metaflac.value)

    tags = {}
    for tag in TAGS:

        # Invokes the 'metaflac' program with the following arguments:
        # --show-tag => Shows the value of the given tag
        p = Popen([Programs.metaflac.value, '--show-tag=' + tag, filename], stdout=PIPE)
        value = p.stdout.read().decode(ENCODING).rstrip('\n')
        if value:
            tags[tag] = value.split('=')[1]

    return tags


# Methods :: File management
# --------------------------------------------------------------------------------------------------
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


# Methods :: External program validation
# --------------------------------------------------------------------------------------------------
def is_program_available(program):
    """
    Checks if an external program is present in the operating system.
    :param program: The name of the external program
    :return: True if the program is present in the operating system; False otherwise
    """
    # The output of the following command should be something like:
    # flac: /usr/bin/flac /usr/share/man/man1/flac.1.gz
    output = Popen(['whereis', program], stdout=PIPE).communicate()[0]
    if len(output.split()) == 1:
        _logger.error(ERROR_PROGRAM_NOT_FOUND.format(program))
        sys.exit(1)
