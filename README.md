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

(The MIT License)

Copyright © 2012 Eduardo Ferreira

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
