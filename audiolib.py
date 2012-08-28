#!/usr/bin/python -tt

# Module import section
# -------------------------------------------------------------------------------------------------
from subprocess import call, PIPE, Popen
from os.path import basename, join, splitext


# Constants :: Lists and file extensions
# -------------------------------------------------------------------------------------------------
TAG_NAMES = ["TITLE", "ARTIST", "ALBUM", "DATE", "TRACKNUMBER", "TRACKTOTAL", "GENRE"]
TAG_FLAGS = ["--tt", "--ta", "--tl", "--ty", "--tn", "--tg"]
EXT_FLAC = ".flac"
EXT_MP3 = ".mp3"
EXT_WAV = ".wav"


# Methods :: File encoding and decoding
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Retrieves and stores the ID3 tag values of a FLAC audio file.
#
# @param filename FLAC audio file name
# @return The values of the metatags
# *************************************************************************************************
def get_tags(filename):
	tag_values = []
	for tag_name in TAG_NAMES:

		# Prepares the 'sed' program arguments
		sed = ["sed", "s/.*=//"]

		# Invokes the 'metaflac' and 'sed' programs to retrieve the ID3 tag values
		p1 = Popen(["metaflac", "--show-tag=" + tag_name, filename], stdout=PIPE)
		p2 = Popen(sed, stdin=p1.stdout, stdout=PIPE)
		tag_values.append(p2.communicate()[0].rstrip("\n"))

	return tag_values


# *************************************************************************************************
# Decodes a FLAC audio file, generating the corresponding WAV audio file and storing its ID3 tags.
#
# @param filename FLAC audio file name
# @return The values of the metatags
# *************************************************************************************************
def decode_flac(filename):

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
def encode_wav_flac(filename, tag_values):

	# Prepares the ID3 tags to be passed as parameters of the 'flac' program
	id3_flags = ["-T", "TITLE=" + tag_values[0], "-T", "ARTIST=" + tag_values[1], "-T", "ALBUM=" +
				tag_values[2], "-T", "DATE=" + tag_values[3], "-T", "TRACKNUMBER=" + tag_values[4],
				"-T", "TRACKTOTAL=" + tag_values[5], "-T", "GENRE=" + tag_values[6]]

	# Prepares the 'flac' program arguments:
	# -f => Force overwriting of output files
	# -8 => Synonymous with -l 12 -b 4096 -m -e -r 6
	# -V => Verify a correct encoding
	flac = ["flac", "-f8V"]
	flac.extend(id3_flags)

	# Replaces the extension of the input file (from FLAC to WAV)
	flac.append(splitext(filename)[0] + EXT_WAV)

	# Invokes the 'flac' program to encode the WAV audio file with the given ID3 tags
	call(flac)


# *************************************************************************************************
# Encodes a WAV audio file, generating the corresponding MP3 audio file and storing its ID3 tags.
#
# @param filename WAV audio file name
# @param tag_values Values of the ID3 tags
# @param destination Destination folder where the resulting MP3 file will be stored
# *************************************************************************************************
def encode_wav_mp3(filename, tag_values, destination=""):

	# Prepares the ID3 tags to be passed as parameters of the 'lame' program
	id3_flags = ["--tt", tag_values[0], "--ta", tag_values[1], "--tl", tag_values[2],
				"--ty", tag_values[3], "--tn", tag_values[4] + "/" + tag_values[5],
				"--tg", tag_values[6]]

	# Prepares the 'lame' program arguments:
	# -b 320          => Set the bitrate to 320 kbps
	# -q 0            => Highest quality, very slow
	# --preset insane => Type of the quality settings
	# --id3v2-only    => Add only a version 2 tag
	lame = ["lame", "-b", "320", "-q", "0", "--preset", "insane", "--id3v2-only"]
	lame.extend(id3_flags)

	# Replaces the extension of the input file (from FLAC to WAV)
	lame.append(splitext(filename)[0] + EXT_WAV)

	# Updates the path of the output file to match the given destination folder and replaces its
	# extension (from FLAC to MP3)
	new_filename = basename(filename)
	new_filename = splitext(new_filename)[0]
	new_filename = join(destination, new_filename)
	lame.append(new_filename + EXT_MP3)

	# Invokes the 'lame' program to encode the WAV audio file with the given ID3 tags
	# FLAC => WAV => MP3
	call(lame)


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
	rm.append(splitext(filename)[0] + audiolib.EXT_WAV)

	# Invokes the 'rm' program to remove the temporary WAV audio file
	call(rm)
