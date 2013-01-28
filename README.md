# FLAC Manager

A set of simple Python programs that allow a user to manage the conversion
between several types of audio files.

## Programs

* `wav2flac` (lossless => lossless)  
Encodes WAV files into the FLAC format with the maximum compression level.
* `wav2mp3` (lossless => lossy)  
Encodes WAV files into the MP3 format with the maximum compression level.
* `flac2wav` (lossless => lossless)  
Decodes FLAC files into the WAV format.
* `flac2mp3` (lossless => lossy)  
Encodes FLAC files into the MP3 format with the maximum compression level.

## Instructions

Each of the programs provides the same set of options:

* -f => Specify a set of files to convert
* -F => Folder with a set of files to convert
* -d => Folder in which the generated MP3 files will be saved
* -h => Display a help message with detailed information regarding the script
* -v => Output the current version

The current syntax requires that both the location of the input and output files
be defined explicitly:

	[program] [-fF] [input-file(s)] [-d] [destination]

## Examples

A specific WAV file is selected and the resulting FLAC file will be stored in
the given folder.

	wav2flac -f lovely_song.wav -d ~/new_songs/

A folder with a set of WAV files is selected and the resulting MP3 files will
be stored in the given folder.

	wav2mp3 -F ~/songs/ -d ~/new_songs/

## Versions

Version 0.1.1

* First stable iteration
* Added the "-h", "-v", "-d", "-f" and "-F" options
* Refactored major portions of the code, mostly by replacing "hand made" code
with Python built-in functions

Version 0.1.0

* Initial version

## Roadmap

Version 0.2.0 will have the following features:

* `flac2wav` will save any metadata present in ID3 tags to a text file and the
album cover to an image file while decoding the given FLAC files
* `wav2flac` will have two additional command line arguments to import a text
file with ID3 tags and an image file with an album cover

## License

Copyright © 2012-2013 Eduardo Ferreira

The code in this repository is MIT licensed, and therefore free to use as you
please for commercial or non-commercial purposes (see LICENSE for details).
