#!/usr/bin/python -tt

# Module import section
# -------------------------------------------------------------------------------------------------
import collections
import errno
import os
import re
import subprocess
import sys

# Constants
# -------------------------------------------------------------------------------------------------
TAG_NAMES = ['TITLE', 'ARTIST', 'ALBUM', 'DATE', 'TRACKNUMBER', 'TRACKTOTAL', 'GENRE']
TAG_FLAGS = ['--tt', '--ta', '--tl', '--ty', '--tn', '--tg']


# Methods :: Folder and file library
# -------------------------------------------------------------------------------------------------

# *************************************************************************************************
# Checks if a folder contains, at least, one file.
#
# @param folder Folder to check for files
# @return True if the folder contains any files; False otherwise
# *************************************************************************************************
def folder_has_files(folder):
	for item in os.listdir(folder):
		item_path = os.path.join(folder, item)
		if os.path.isfile(item_path):
			return True

	return False


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
		p1 = subprocess.Popen(["metaflac", "--show-tag=" + tag_name, filename], stdout=subprocess.PIPE)
		p2 = subprocess.Popen(sed, stdin=p1.stdout, stdout=subprocess.PIPE)
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
	flac = ["flac", "-d", filename]

	# Invokes the 'flac' program to decode the FLAC audio file and retrieves the ID3 tags
	subprocess.call(flac)
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
	# -c => Write output to stdout
	# -8 => Synonymous with -l 12 -b 4096 -m -e -r 6
	# -V => Verify a correct encoding
	flac = ["flac", "-c8V"]
	flac.extend(id3_flags)
	flac.append(filename.rstrip(".flac").join(".wav"))

	# Invokes the 'flac' program to encode the WAV audio file with the given ID3 tags
	subprocess.call(flac)


# *************************************************************************************************
# Encodes a WAV audio file, generating the corresponding MP3 audio file and storing its ID3 tags.
#
# @param filename WAV audio file name
# @param tag_values Values of the ID3 tags
# *************************************************************************************************
def encode_wav_mp3(filename, tag_values):

	# Prepares the ID3 tags to be passed as parameters of the 'lame' program
	id3_flags = ['--tt', tag_values[0], '--ta', tag_values[1], '--tl', tag_values[2],
				'--ty', tag_values[3], '--tn', tag_values[4] + "/" + tag_values[5],
				'--tg', tag_values[6]]

	# Prepares the 'lame' program arguments
	lame = ["lame", "-b", "320", "-q", "0", "--preset", "insane", "--add-id3v2"]
	lame.extend(id3_flags)
	lame.append(filename.rstrip(".flac").join(".wav"))

	# Invokes the 'lame' program to encode the WAV audio file with the given ID3 tags
	# FLAC => WAV => MP3
	subprocess.call(lame)


# *************************************************************************************************
# Main function
# *************************************************************************************************
def main():
	tags = decode_flac(sys.argv[1])
	encode_wav_flac(sys.argv[1], tags)
	encode_wav_mp3(sys.argv[1], tags)


# Standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()
