#!/usr/bin/python -tt

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
# @return The values of the metatags
# *************************************************************************************************
def decode_flac_wav(filename):

	# Prepares the 'flac' program arguments:
	# -d => Decode (the default behavior is to encode)
	# -f => Force overwriting of output files
	flac = ["flac", "-d", "-f", filename]

	# Invokes the 'flac' program to decode the FLAC audio file and retrieves the ID3 tags
	call(flac)
	tag_values = get_tags(filename)

	return tag_values


# *************************************************************************************************
# Encodes a WAV audio file, generating the corresponding FLAC audio file and storing its ID3 tags.
#
# @param filename WAV audio file name
# @param tag_values Values of the ID3 tags
# *************************************************************************************************
def encode_wav_flac(filename, tag_values=[]):

	# Prepares the 'flac' program arguments:
	# -f => Force overwriting of output files
	# -8 => Synonymous with -l 12 -b 4096 -m -e -r 6
	# -V => Verify a correct encoding
	flac = ["flac", "-f8V"]

	# Prepares the ID3 tags to be passed as parameters of the 'flac' program
	if tag_values:
		id3_flags = ["-T", "TITLE=" + tag_values[0], "-T", "ARTIST=" + tag_values[1], "-T", "ALBUM=" +
					tag_values[2], "-T", "DATE=" + tag_values[3], "-T", "TRACKNUMBER=" + tag_values[4],
					"-T", "TRACKTOTAL=" + tag_values[5], "-T", "GENRE=" + tag_values[6]]

		flac.extend(id3_flags)

	# Replaces the extension of the input file (from FLAC to WAV)
	#flac.append(splitext(filename)[0] + EXTENSIONS["wav"])
	flac.append(filename)

	# Invokes the 'flac' program to encode the WAV audio file with the given ID3 tags
	call(flac)


# *************************************************************************************************
# Encodes a WAV audio file, generating the corresponding MP3 audio file and storing its ID3 tags.
#
# @param filename WAV audio file name
# @param tag_values Values of the ID3 tags
# @param cover Name of the cover file
# @param destination Destination folder where the resulting MP3 file will be stored
# *************************************************************************************************
def encode_wav_mp3(filename, tag_values, cover, destination=""):

	# Prepares the ID3 tags to be passed as parameters of the 'lame' program
	id3_flags = ["--tt", tag_values[0], "--ta", tag_values[1], "--tl", tag_values[2],
				"--ty", tag_values[3], "--tn", tag_values[4] + "/" + tag_values[5],
				"--tg", tag_values[6]]

	# Checks if the audio file has a cover
	if not isstringempty(cover):
		id3_flags.extend(["--ti", cover])

	# Prepares the 'lame' program arguments:
	# -b 320          => Set the bitrate to 320 kbps
	# -q 0            => Highest quality, very slow
	# --preset insane => Type of the quality settings
	# --id3v2-only    => Add only a version 2 tag
	lame = ["lame", "-b", "320", "-q", "0", "--preset", "insane", "--id3v2-only"]
	lame.extend(id3_flags)

	# Replaces the extension of the input file (from FLAC to WAV)
	lame.append(splitext(filename)[0] + EXTENSIONS["wav"])

	# Updates the path of the output file to match the given destination folder and replaces its
	# extension (from FLAC to MP3)
	new_filename = basename(filename)
	new_filename = splitext(new_filename)[0]
	new_filename = join(destination, new_filename)
	lame.append(new_filename + EXTENSIONS["mp3"])

	# Invokes the 'lame' program to encode the WAV audio file with the given ID3 tags
	call(lame)


# Methods :: File cleanup
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
