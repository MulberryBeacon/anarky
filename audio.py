#!/usr/bin/python -tt
# -*- coding: utf8 -*-

"""
Audio library with conversion methods.

Author: Eduardo Ferreira
License: MIT (see LICENSE for details)
"""

# Module import section
# ----------------------------------------------------------------------------------------------------------------------
from miscellaneous import is_string_empty
from os.path import basename, join, splitext
from subprocess import call, PIPE, Popen

# Constants :: Lists and file extensions
# ----------------------------------------------------------------------------------------------------------------------
PLAYLIST = "00. {0} - {1}.m3u"
TAGS_FILE = "tags.txt"

"""
TITLE       : Track/Work name
ARTIST      : The artist generally considered responsible for the work. In popular music this is usually the performing
			  band or singer. For classical music it would be the composer. For an audio book it would be the author of
			  the original text
ALBUM       : The collection name to which this track belongs
TRACKNUMBER : The track number of this piece if part of a specific larger collection or album
ALBUMARTIST : The artist(s) who performed the work. In classical music this would be the conductor, orchestra, soloists.
			  In an audio book it would be the actor who did the reading. In popular music this is typically the same as
			  the ARTIST and is omitted
GENRE       : A short text indication of music genre
DATE        : Date the track was recorded
DISCTOTAL   : Number of discs that compose the set ("DISCTOTAL" : ["--tv", "TPOS="],)
TRACKTOTAL  : Number of tracks in the album
"""
TAGS = {
	"TITLE"      : "--tt",
	"ARTIST"     : "--ta",
	"ALBUM"      : "--tl",
	"TRACKNUMBER": "--tn",
	"ALBUMARTIST": ["--tv", "TPE2="],
	"GENRE"      : "--tg",
	"DATE"       : "--ty",
	"TRACKTOTAL" : ""
}

EXTENSIONS = {
	"flac": ".flac",
	"mp3" : ".mp3",
	"wav" : ".wav"
}

# Methods :: Album cover and ID3 tag management
# ----------------------------------------------------------------------------------------------------------------------
def get_cover(filename, destination):
	"""
	Retrieves the cover file from a FLAC audio file.
	"""
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

	# Checks if the audio file has a cover. If so, retrieves it
	if not is_string_empty(cover):

		# Prepares the 'metaflac' program arguments:
		# --export-picture-to => Export PICTURE block to a file
		cover = join(destination, cover)
		metaflac = ["metaflac", "--export-picture-to=" + cover, filename]
		call(metaflac)

	return cover


def set_cover(filename, cover):
	"""
	Imports a cover file to a FLAC audio file.
	"""
	# Prepares the 'metaflac' program arguments:
	# --import-picture-to => Import a picture and store it in a PICTURE block
	specification = "||" + basename(cover) + "||" + cover
	metaflac = ["metaflac", "--import-picture-from=" + specification, filename]
	call(metaflac)


def get_tags(filename, destination):
	"""
	Retrieves and stores the ID3 tag values of a FLAC audio file.
	"""
	tags = {}
	for tag in TAGS:

		# Prepares the 'metaflac' program arguments:
		# --show-tag => Shows the value of the given tag
		metaflac = ["metaflac", "--show-tag=" + tag, filename]

		# Prepares the 'sed' program arguments (the regular expression removes the tag name)
		sed = ["sed", "s/.*=//"]

		# Invokes the 'metaflac' and 'sed' programs to retrieve the ID3 tag values
		p1 = Popen(metaflac, stdout=PIPE)
		p2 = Popen(sed, stdin=p1.stdout, stdout=PIPE)
		tags[tag] = p2.communicate()[0].rstrip("\n")

	# Creates a tag file
	create_tag_file(filename, destination)

	return tags


# Methods :: File encoding and decoding
# ----------------------------------------------------------------------------------------------------------------------
def decode_flac_wav(filename, destination, cover=False, tags=False):
	"""
	Decodes a FLAC audio file, generating the corresponding WAV audio file.
	Also retrieves the list of its ID3 tags and album cover.
	"""
	# Prepares the 'flac' program arguments:
	# -d => Decode (the default behavior is to encode)
	# -f => Force overwriting of output files
	flac = ["flac", "-d", "-f", filename]

	# Updates the path of the output file to match the given destination folder
	new_filename = ""
	if not is_string_empty(destination):
		new_filename = splitext(join(destination, basename(filename)))[0]
		flac.extend(["-o", new_filename + EXTENSIONS["wav"]])

	# Invokes the 'flac' program to decode the FLAC audio file and retrieves the ID3 tags
	call(flac)

	# Checks if both cover and tags should be retrieved
	cover_value = (get_cover(filename, destination) if cover else None)
	tags_value = get_tags(filename, destination) if tags else None

	return (cover_value, tags_value)


def encode_wav_flac(filename, destination, cover, tags):
	"""
	Encodes a WAV audio file, generating the corresponding FLAC audio file.
	"""
	# Prepares the 'flac' program arguments:
	# -f => Force overwriting of output files
	# -8 => Synonymous with -l 12 -b 4096 -m -e -r 6
	# -V => Verify a correct encoding
	flac = ["flac", "-f8V"]

	# Prepares the ID3 tags to be passed as parameters of the 'flac' program
	if tags:
		for tag in TAGS:
			flac.extend(["-T", tag + "=" + tags[tag]])

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


def encode_wav_mp3(filename, destination, cover, tags):
	"""
	Encodes a WAV audio file, generating the corresponding MP3 audio file.
	"""
	# Prepares the 'lame' program arguments:
	# -b 320          => Set the bitrate to 320 kbps
	# -q 0            => Highest quality, very slow
	# --preset insane => Type of the quality settings
	# --id3v2-only    => Add only a version 2 tag
	lame = ["lame", "-b", "320", "-q", "0", "--preset", "insane", "--id3v2-only"]

	# Prepares the ID3 tags to be passed as parameters of the 'lame' program
	if tags:
		for tag in TAGS:
			if tag in ["ALBUMARTIST", "DISCTOTAL"]:
				pair = TAGS[tag]
				lame.extend([pair[0], pair[1] + tags[tag]])

			elif tag != "TRACKTOTAL":
				tracktotal = ("/" + tags["TRACKTOTAL"]) if tag == "TRACKNUMBER" else ""
				lame.extend([TAGS[tag], tags[tag] + tracktotal])

	# Checks if the audio file has a cover
	if not is_string_empty(cover):
		lame.extend(["--ti", cover])

	# Updates the path of the output file to match the given destination folder
	lame.append(filename)
	if not is_string_empty(destination):
		lame.append(splitext(join(destination, basename(filename)))[0] + EXTENSIONS["mp3"])

	# Invokes the 'lame' program to encode the WAV audio file
	call(lame)


def encode_flac_mp3(filename, destination, cover="", tags={}):
	"""
	Decodes a FLAC audio file, generating the corresponding WAV audio file.
	The WAV audio file is then encoded, generating the corresponding MP3 audio file.
	"""
	get_cover = True if is_string_empty(cover) else False
	get_tags = True if len(tags) == 0 else False
	(new_cover, new_tags) = decode_flac_wav(filename, destination, get_cover, get_tags)
	new_filename = splitext(join(destination, basename(filename)))[0] + EXTENSIONS["wav"]
	encode_wav_mp3(new_filename, destination, (new_cover if get_cover else cover), (new_tags if get_tags else tags))


# Methods :: File management
# ----------------------------------------------------------------------------------------------------------------------
def cleanup(filename):
	"""
	Removes the temporary WAV audio file created during the conversion process.
	"""
	# Prepares the 'rm' program arguments:
	# -r => Remove directories and their contents recursively
	# -f => Ignore nonexistent files, never prompt
	rm = ["rm", "-rf"]

	# Replaces the extension of the input file (from FLAC to WAV)
	rm.append(splitext(filename)[0] + EXTENSIONS["wav"])

	# Invokes the 'rm' program to remove the temporary WAV audio file
	call(rm)


def create_playlist(folder, artist, album):
	"""
	Creates a playlist file (.m3u extension) for the given album.
	"""
	# Prepares the 'ls' program arguments
	ls = ["ls", folder]

	# Creates a new file with the specified name and writes the list of files
	with open(join(folder, PLAYLIST.format(artist, album)), 'w') as output:
		p = Popen(ls, stdout=output)

	output.close()


def create_tag_file(filename, destination):
	"""
	Creates an ID3 tag file (.txt extension) for the given audio file.
	"""
	# Prepares the 'metaflac' program arguments:
	# --export-tags-to => Export tags to a file (use '-' for stdout)
	metaflac = ["metaflac", "--export-tags-to=-", filename]
	p = Popen(metaflac, stdout=PIPE)
	tags = [(tag[0:tag.index('=')].upper() + tag[tag.index('='):]) for tag in p.communicate()[0].rstrip("\n").split("\n")]

	# Writes the list of tags to the file
	stream = open(join(destination, TAGS_FILE), 'a')
	new_filename = splitext(join(destination, basename(filename)))[0] + EXTENSIONS["wav"]
	tags.insert(0, new_filename)
	stream.write('|'.join(tags) + '\n')
	stream.close()


def read_tag_file(filename):
	"""
	Reads the contents of an ID3 tag text file.
	"""
	stream = open(filename, 'r')
	result = {}
	for line in stream:
		list_tags = line.rstrip('\n').split('|')
		map_tags = {}
		for tag in list_tags[1:]:
			(flac, value) = tag.split('=')
			map_tags[flac] = value

		result[list_tags[0]] = map_tags

	stream.close()
	return result
