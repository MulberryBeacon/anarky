FlacToMp3
=========

A simple Python script that takes a list of FLAC files and performs the
following operations for each file:
* Decodes the FLAC file and saves (if any) the metadata present in ID3 tags;
* Converts the resulting WAV file to MP3, using the maximum compression level
and the metadata retrieved in the previous step;
* Encodes the FLAC file with the maximum compression level;
* Removes the previously extracted WAV files.

Versions
--------

* version 0.1.1
	* First stable iteration
	* Added the "-h", "-v", "-d", "-f" and "-F" options
	* Refactored major portions of the code, mostly by replacing "hand made"
	code by Python built-in functions

* version 0.1.0
	* Initial version

Roadmap
-------

Version 0.1.1 will have the following features:
* Ability to save the generated MP3 files in a new folder. The user will be
able to define the path to the MP3 folder as a command line argument (-d flag).
* Broaden the range of command line options:
	* Currently, the user can only pass one file name as an argument (if no file
	is given or the argument is not a file, the program crashes);
	* Allow for one or more file names as arguments (-f flag);
	* If no file names are given, the program will go through the contents of
	the current folder and convert any FLAC files it finds;
* Global file checking and exception handling.

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