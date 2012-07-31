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

* version 0.1.0
	* Initial version

Roadmap
-------

Version 0.1.1 will have the following features:
* Ability to save the generated MP3 files in a new folder. The user will be
able to define the path to the MP3 folder as a command line argument.

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