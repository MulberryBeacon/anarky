FlacToMp3
=========

A simple Python script that takes a list of FLAC files and performs the
following operations for each file:

* Decodes the FLAC file and saves (if any) the metadata present in ID3 tags;
* Converts the resulting WAV file to MP3, using the maximum compression level
and the metadata retrieved in the previous step;
* Encodes the FLAC file with the maximum compression level;
* Removes the previously extracted WAV files.

Instructions
------------

The script can be invoked by using the following syntax:

	flactomp3 [-f] [filenames] [-d] [folder]

The available options are:

* -f => Specify a set of files to convert
* -F => Folder with a set of files to convert
* -d => Folder in which the generated MP3 files will be saved
* -h => Display a help message with detailed information regarding the script
* -v => Output the current version

Examples
--------

A specific FLAC file is selected and the resulting MP3 file will be stored in
the current folder (where the script is run).

	flactomp3 -f lovely_song.flac

A specific FLAC file is selected and the resulting MP3 file will be stored in
the given folder.

	flactomp3 -f lovely_song.flac -d ~/new_songs/

A folder with a set of FLAC files is selected and the resulting MP3 files will
be stored in the given folder.

	flactomp3 -F ~/songs/ -d ~/new_songs/

A specific FLAC file and a folder with a set of FLAC files are selected, with
the resulting MP3 files being stored in the given folder.

	flactomp3 -f lovely_song.flac -F ~/lovely_songs/ -d ~/new_songs/

Versions
--------

Version 0.1.1

* First stable iteration
* Added the "-h", "-v", "-d", "-f" and "-F" options
* Refactored major portions of the code, mostly by replacing "hand made" code
with Python built-in functions

Version 0.1.0

* Initial version

Roadmap
-------

Version 0.1.1 will have the following features:

* Broaden the range of command line options:
	* If no file names are given, the program will go through the contents of
	the current folder and convert any FLAC files it finds;

Version 0.1.2 will have the following features:

* New round of deep testing, bug fixing and code normalization;
* Add the album cover to the set of metadata copied from FLAC to MP3 files;
* Global file checking and exception handling.

License
-------

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
