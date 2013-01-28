#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Audio library with conversion methods.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import section
# -------------------------------------------------------------------------------------------------
from miscellaneous import is_string_empty
from os.path import basename, join, splitext
from subprocess import call, PIPE, Popen


# Constants :: Lists and file extensions
# -------------------------------------------------------------------------------------------------
TAG_NAMES = ["TITLE", "ARTIST", "ALBUM", "DATE", "TRACKNUMBER", "TRACKTOTAL", "GENRE"]
TAG_FLAGS = ["--tt", "--ta", "--tl", "--ty", "--tn", "--tg"]
EXTENSIONS = {"flac": ".flac", "mp3": ".mp3", "wav": ".wav"}
PLAYLIST = "00. {0} - {1}"


# Methods :: Album cover and ID3 tag management
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Retrieves the cover file from a FLAC audio file.
#
# @param filename FLAC audio file name
# @return The name of the cover file
# *************************************************************************************************
def get_cover(filename):

	# Prepares the 'metaflac' program arguments:
	# --list       => Lists the full stack of metadata
	# --block-type => Comma-separated list of block types to be included
	metaflac = ["metaflac", "--list", "--block-type=PICTURE", filename]

	# Prepares the 'grep' program arguments (looks for description parameter)
	grep = ["grep", "description:"]

	# Prepares the 'sed' program arguments (the regular expression removes the parameter name)
	sed = ["sed", "s/.*: //"]

	# Invokes the 'metaflac', 'grep' and 'sed' programs to retrieve the cover file name
	p1 = Popen(metaflac, stdout=PIPE)
	p2 = Popen(grep, stdin=p1.stdout, stdout=PIPE)
	p3 = Popen(sed, stdin=p2.stdout, stdout=PIPE)
	cover = p3.communicate()[0].rstrip("\n")

	# Checks if the audio file has a cover
	if not is_string_empty(cover):

		# Prepares the 'metaflac' program arguments:
		# --export-picture-to => Export PICTURE block to a file
		metaflac = ["metaflac", "--export-picture-to=" + cover, filename]

		# Invokes the 'metaflac' program to retrieve the cover file
		call(metaflac)

	return cover


# *************************************************************************************************
# Imports a cover file to a FLAC audio file.
#
# @param filename FLAC audio file name
# @param cover Cover file name
# *************************************************************************************************
def set_cover(filename, cover):

	# Prepares the 'metaflac' program arguments:
	# --import-picture-to => Import a picture and store it in a PICTURE block
	metaflac = ["metaflac", "--import-picture-from=" + cover, filename]

	# Invokes the 'metaflac' program to import the cover file
	call(metaflac)


# *************************************************************************************************
# Retrieves and stores the ID3 tag values of a FLAC audio file.
#
# @param filename FLAC audio file name
# @return The values of the metatags
# *************************************************************************************************
def get_tags(filename):
	tag_values = []
	for tag_name in TAG_NAMES:

		# Prepares the 'metaflac' program arguments:
		# --show-tag => Shows the value of the given tag
		metaflac = ["metaflac", "--show-tag=" + tag_name, filename]

		# Prepares the 'sed' program arguments (the regular expression removes the tag name)
		sed = ["sed", "s/.*=//"]

		# Invokes the 'metaflac' and 'sed' programs to retrieve the ID3 tag values
		p1 = Popen(metaflac, stdout=PIPE)
		p2 = Popen(sed, stdin=p1.stdout, stdout=PIPE)
		tag_values.append(p2.communicate()[0].rstrip("\n"))

	return tag_values


# Methods :: File encoding and decoding
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Decodes a FLAC audio file, generating the corresponding WAV audio file and storing its ID3 tags.
#
# @param filename FLAC audio file name
# @param destination Destination folder where the resulting FLAC file will be stored
# @return The values of the metatags
# *************************************************************************************************
def decode_flac_wav(filename, destination=""):

	# Prepares the 'flac' program arguments:
	# -d => Decode (the default behavior is to encode)
	# -f => Force overwriting of output files
	flac = ["flac", "-d", "-f", filename]

	# Updates the path of the output file to match the given destination folder
	if not is_string_empty(destination):
		flac.extend(["-o", splitext(join(destination, basename(filename)))[0] + EXTENSIONS["wav"]])

	# Invokes the 'flac' program to decode the FLAC audio file and retrieves the ID3 tags
	call(flac)

	return get_tags(filename)


# *************************************************************************************************
# Encodes a WAV audio file, generating the corresponding FLAC audio file and storing its ID3 tags.
#
# @param filename WAV audio file name
# @param destination Destination folder where the resulting FLAC file will be stored
# @param tags Values of the ID3 tags
# @param cover Name of the cover file
# *************************************************************************************************
def encode_wav_flac(filename, destination="", tags=[], cover=""):

	# Prepares the 'flac' program arguments:
	# -f => Force overwriting of output files
	# -8 => Synonymous with -l 12 -b 4096 -m -e -r 6
	# -V => Verify a correct encoding
	flac = ["flac", "-f8V"]

	# Prepares the ID3 tags to be passed as parameters of the 'flac' program
	if tags:
		flac.extend(["-T", "TITLE=" + tags[0], "-T", "ARTIST=" + tags[1], "-T", "ALBUM=" + tags[2],
					"-T", "DATE=" + tags[3], "-T", "TRACKNUMBER=" + tags[4], "-T", "TRACKTOTAL=" +
					tags[5], "-T", "GENRE=" + tags[6]])

	# Updates the path of the output file to match the given destination folder
	flac.append(filename)
	new_filename = splitext(filename)[0] + EXTENSIONS["flac"]
	if not is_string_empty(destination):
		new_filename = join(destination, basename(new_filename))
		flac.extend(["-o", new_filename])

	# Invokes the 'flac' program to encode the WAV audio file
	call(flac)

	# Checks if the audio file has a cover
	if not is_string_empty(cover):
		set_cover(new_filename, cover)


# *************************************************************************************************
# Encodes a WAV audio file, generating the corresponding MP3 audio file and storing its ID3 tags.
#
# @param filename WAV audio file name
# @param destination Destination folder where the resulting MP3 file will be stored
# @param tags Values of the ID3 tags
# @param cover Name of the cover file
# *************************************************************************************************
def encode_wav_mp3(filename, destination="", tags=[], cover=""):

	# Prepares the 'lame' program arguments:
	# -b 320          => Set the bitrate to 320 kbps
	# -q 0            => Highest quality, very slow
	# --preset insane => Type of the quality settings
	# --id3v2-only    => Add only a version 2 tag
	lame = ["lame", "-b", "320", "-q", "0", "--preset", "insane", "--id3v2-only"]

	# Prepares the ID3 tags to be passed as parameters of the 'lame' program
	if tags:
		lame.extend(["--tt", tags[0], "--ta", tags[1], "--tl", tags[2], "--ty", tags[3], "--tn",
					tags[4] + "/" + tags[5], "--tg", tags[6]])

	# Checks if the audio file has a cover
	if not is_string_empty(cover):
		lame.extend(["--ti", cover])

	# Updates the path of the output file to match the given destination folder
	lame.append(filename)
	if not is_string_empty(destination):
		lame.append(splitext(join(destination, basename(filename)))[0] + EXTENSIONS["mp3"])

	# Invokes the 'lame' program to encode the WAV audio file
	call(lame)


# *************************************************************************************************
# Decodes a FLAC audio file, generating the corresponding WAV audio file and storing its ID3 tags.
# The WAV audio file is then encoded, generating the corresponding MP3 audio file and storing its
# ID3 tags.
#
# @param filename WAV audio file name
# @param destination Destination folder where the resulting MP3 file will be stored
# *************************************************************************************************
def encode_flac_mp3(filename, destination=""):
	cover = get_cover(filename)
	tags = decode_flac_wav(filename)
	new_filename = splitext(filename)[0] + EXTENSIONS["wav"]
	encode_wav_mp3(new_filename, destination, tags, cover)


# Methods :: File management
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Removes the temporary WAV audio file created during the conversion process.
#
# @param filename File to remove
# *************************************************************************************************
def cleanup(filename):

	# Prepares the 'rm' program arguments:
	# -r => Remove directories and their contents recursively
	# -f => Ignore nonexistent files, never prompt
	rm = ["rm", "-rf"]

	# Replaces the extension of the input file (from FLAC to WAV)
	rm.append(splitext(filename)[0] + EXTENSIONS["wav"])

	# Invokes the 'rm' program to remove the temporary WAV audio file
	call(rm)


# *************************************************************************************************
# Creates a playlist file (.m3u extension) for the given album.
#
# @param folder Folder that contains an album
# @param artist Artist name
# @param album Album name
# *************************************************************************************************
def create_playlist(folder, artist, album):

	# Prepares the 'ls' program arguments
	ls = ["ls", folder]

	# Creates a new file with the specified name and writes the list of files
	with open(PLAYLIST.format(artist, album), 'w') as output:
		p = Popen(ls, stdout=output)
