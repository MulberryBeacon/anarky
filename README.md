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

The `wav2flac` and `wav2mp3` programs provide the same set of options:

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -c IMG, --cover IMG   add an image file with a cover
      -t TAGS, --tags TAGS  add ID3 tags with the main information
      -p, --playlist        create a playlist file

    options:
      -f FILE [FILE ...], --files FILE [FILE ...]
                            set of files to convert
      -d DEST, --dest DEST  directory in which the generated files will be saved

The `flac2wav` program provides a marginally smaller set of options, since that creating a playlist file isn't necessary during a decoding operation. Also, the "-c" and "-t" options don't require a value because any cover art and ID3 tags should be retrieved from audio files instead of added to them:

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -c, --cover           extract an image file with a cover
      -t, --tags            extract ID3 tags with the main information

    options:
      -f FILE [FILE ...], --files FILE [FILE ...]
                            set of files to convert
      -d DEST, --dest DEST  directory in which the generated files will be saved

The `flac2mp3` program is under review and it's currently *not working*.

The current syntax requires that both the location of the input and output files be defined explicitly:

    PROGRAM [-h] [-v] -f FILE [FILE ...] -d DEST [-c] [-t]

## Examples

A specific WAV file is selected and the resulting FLAC file will be stored in the given folder.

    wav2flac -f lovely_song.wav -d ~/new_songs/

A specific FLAC file is selected and the resulting WAV file will be stored in the given folder, along with the extracted cover art and ID3 tags files.

    wav2flac -f lovely_song.wav -d ~/new_songs/ -c -t

## Versions

See [CHANGELOG](CHANGELOG.md) for details.

## Bugs

* `flac2mp3` doesn't remove the temporary files that are extracted from the input FLAC files (WAV and cover art files). Code still needs to be implement to perform this step

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
