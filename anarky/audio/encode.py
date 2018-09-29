# -*- coding: utf8 -*-

"""
Audio encoding operations.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

from subprocess import call

from anarky.audio.decode import decode_flac_wav
from anarky.enum.program import Program
from anarky.enum.audio_file import AudioFile
from anarky.utils import update_path


def encode_wav_flac(filename: str, destination: str) -> str:
    """
    Encodes a WAV audio file, generating the corresponding FLAC audio file.

    The 'flac' program is executed with the following arguments:
      * -f => Force overwriting of output files
      * -8 => Synonymous with -l 12 -b 4096 -m -e -r 6
      * -V => Verify a correct encoding
      * -o => Force the output file name

    :param filename:
        The input audio file name
    :param destination:
        The destination where the output file will be stored
    :return:
        The name of the output audio file
    """
    output_filename = update_path(filename, destination, AudioFile.FLAC.value)
    call([Program.FLAC.value, '-f8V', '-o', output_filename, filename])

    return output_filename


def encode_wav_mp3(filename: str, destination: str) -> str:
    """
    Encodes a WAV audio file, generating the corresponding MP3 audio file.

    The 'lame' program is executed with the following arguments:
      * -b 320          => Set the bitrate to 320 kbps
      * -q 0            => Highest quality, very slow
      * --preset insane => Type of the quality settings
      * --id3v2-only    => Add only a version 2 tag

    :param filename:
        The input audio file name
    :param destination:
        The destination where the output file will be stored
    :return:
        The name of the output audio file
    """
    output_filename = update_path(filename, destination, AudioFile.MP3.value)
    call([Program.LAME.value, '-b', '320', '-q', '0', '--preset', 'insane', '--id3v2-only', filename, output_filename])

    return output_filename


def encode_flac_mp3(filename: str, destination: str) -> str:
    """
    Decodes a FLAC audio file, generating the corresponding WAV audio file.
    The WAV audio file is then encoded, generating the corresponding MP3 audio file.

    :param filename:
        The input audio file name
    :param destination:
        The destination where the output file will be stored
    :return:
        The name of the output audio file
    """
    wav_file = decode_flac_wav(filename, destination)
    if wav_file:
        return encode_wav_mp3(wav_file[0], destination)

    return None