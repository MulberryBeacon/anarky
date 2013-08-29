# FLAC Manager

A set of simple programs that allow a user to manage the conversion between several types of audio files.

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

For `flac2wav`, the last two options will be used to extract information from files instead of adding it:

    -c, --cover
        extract an image file with a cover
    -t, --tags
        extrac ID3 tags with the main information

The current syntax requires that both the location of the input and output files be defined explicitly:

    [program] [OPTION] [-fd] [input-files] [-e] [destination]

## Examples

A specific WAV file is selected and the resulting FLAC file will be stored in the given folder.

    wav2flac -f lovely_song.wav -e ~/new_songs/

A folder with a set of WAV files is selected and the resulting MP3 files will be stored in the given folder.

    wav2mp3 -d ~/songs/ -e ~/new_songs/

## Versions

See [CHANGELOG](CHANGELOG.md) for details.

## Bugs

* `flac2mp3` doesn't remove the temporary WAV files extracted from the input FLAC files. The code for this is already implemented (albeit pending a review), but it needs to be invoked
* `flac2mp3` doesn't remove the temporary cover file extracted from the input FLAC files. Code still needs to be implement to perform this step

## Roadmap

Future versions will have the following features:

* A new master control program (nudge nudge, wink wink) that could be used instead of the individual programs. It will have two additional options for the desired input and output formats, while keeping the set of options outlined for the current set of programs
* An installation script that will avoid any manual configuration to make the programs globally available in a system (path, location, etc.)
* A synchronization mechanism that can replicate the tree structure of the FLAC folder and automatically convert every album to MP3

## Dependencies

* `lame`
* `flac`
* `metaflac`

## Versioning

This application will be maintained under the Semantic Versioning guidelines as much as possible.

Releases will be numbered with the following format:

`<major>.<minor>.<patch>`

And constructed with the following guidelines:

* Breaking backward compatibility bumps the major (and resets the minor and patch)
* New additions without breaking backward compatibility bumps the minor (and resets the patch)
* Bug fixes and misc changes bumps the patch

For more information on SemVer, please visit [http://semver.org/](http://semver.org/).

## License

Copyright © 2012-2013 Eduardo Ferreira

The code in this repository is MIT licensed, and therefore free to use as you please for commercial or non-commercial purposes (see [LICENSE](LICENSE) for details).
