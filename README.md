# FLAC Manager

A set of simple programs that allow a user to manage the conversion between
several types of audio files.

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

    -f, --file
        set of individual files to convert
    -p, --playlist
        create a playlist file
    -v, --version
        output version information and exit
    -h, --help
        display this help and exit
    -d, --dir
        directory with a set of files to convert
    -e, --dest
        directory in which the generated files will be saved
    -c, --cover
        add an image file with a cover
    -t, --tags
        add ID3 tags with the main information

For `flac2wav`, the last two options will be used to extract information from
files instead of adding it:

    -c, --cover
        extract an image file with a cover
    -t, --tags
        extrac ID3 tags with the main information

The current syntax requires that both the location of the input and output files
be defined explicitly:

    [program] [OPTION] [-fd] [input-files] [-e] [destination]

## Examples

A specific WAV file is selected and the resulting FLAC file will be stored in
the given folder.

    wav2flac -f lovely_song.wav -e ~/new_songs/

A folder with a set of WAV files is selected and the resulting MP3 files will
be stored in the given folder.

    wav2mp3 -d ~/songs/ -e ~/new_songs/

## Versions

Version 0.0.5

* Command line interface is now managed with the `argparse` module
* Simplified the entire audio library

Version 0.0.4

* Added three new options ("-c", "-p" and "-t") and updated the old options
* Further generalization of commnand line related methods and migration to the
interface library
* Refinement of the audio library

Version 0.0.3

* First stable (and working) version
* Generalized some of the commnand line related methods and migrated them to a
new interface library

Version 0.0.2

* Added the "-h", "-v", "-d", "-f" and "-F" options
* Refactored major portions of the code, mostly by replacing "hand made" code
with Python built-in functions

Version 0.0.1

* Initial version

## Bugs

* `flac2mp3` doesn't remove the temporary WAV files extracted from the input
FLAC files. The code for this is already implemented (albeit pending a review),
but it needs to be invoked

* `flac2mp3` doesn't remove the temporary cover file extracted from the input
FLAC files. Code still needs to be implement to perform this step

* Haven't found a way to dynamically define the artist and album names in the
playlist file. For now, the strings "artist" and "album" are used, respectively

## Roadmap

Future versions will have the following features:

* A new master control program (nudge nudge, wink wink) that could be used
instead of the individual programs. It will have two additional options for
the desired input and output formats, while keeping the set of options outlined
for the current set of programs
* An installation script that will avoid any manual configuration to make the
programs globally available in a system (path, location, etc.)
* A synchronization mechanism that can replicate the tree structure of the FLAC
folder and automatically convert every album to MP3

## Dependencies

* `lame`
* `flac`
* `metaflac`

## License

Copyright © 2012-2013 Eduardo Ferreira

The code in this repository is MIT licensed, and therefore free to use as you
please for commercial or non-commercial purposes (see LICENSE for details).
