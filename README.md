# Anarky

A set of simple programs for encoding and decoding between several types of
audio files.

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

The `wav2flac` and `wav2mp3` programs perform an encoding operation and have
the same set of options:

    usage: PROGRAM [-h] [-v] [-p] [-t] [-c IMG] -f FILES [FILES ...] -d DEST

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -p, --playlist        create playlist file
      -t, --tags            add ID3 tags
      -c IMG, --cover IMG   add album art

    options:
      -f FILES [FILES ...], --files FILES [FILES ...]
                            input files to convert
      -d DEST, --dest DEST  output directory for the generated files

The `flac2wav` and `flac2mp3` programs perform a decoding operation (the latter
starts with decoding and then encodes, of course) and have the same set of
options, which is slightly different from the previous two programs due to not
having to provide an album art file:

    usage: PROGRAM [-h] [-v] [-p] [-t] [-c] -f FILES [FILES ...] -d DEST

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -p, --playlist        create playlist file
      -t, --tags            extract ID3 tags
      -c, --cover           extract album art

    options:
      -f FILES [FILES ...], --files FILES [FILES ...]
                            input files to convert
      -d DEST, --dest DEST  output directory for the generated files

The current syntax for the programs requires that the location of both input
and output files be defined explicitly.

## Examples

A specific WAV file is selected and the resulting FLAC file will be stored in
the given folder.

    wav2flac -f lovely_song.wav -d ~/new_songs/

A specific FLAC file is selected and the resulting WAV file will be stored in
the given folder, along with the extracted cover art and ID3 tags file.

    flac2wav -f lovely_song.flac -d ~/new_songs/ -c -t

## Versions

See [CHANGELOG](CHANGELOG.md) for details.

## Dependencies

All development and testing activities are carried out on Mac OS X 10.11.3 using
Python 3.5.1. The following packages are required:

* `lame`
* `flac`
* `metaflac`

## Code metrics

* CLOC

```sh
http://cloc.sourceforge.net v 1.62  T=0.10 s (71.5 files/s, 6550.5 lines/s)
-------------------------------------------------------------------------------
File                             blank        comment           code
-------------------------------------------------------------------------------
./audio.py                          60            116            123
./interface.py                      24             35             52
./wav2mp3.py                         9             13             21
./wav2flac.py                        9             13             21
./flac2wav.py                        8             13             19
./general.py                        15             32             19
./flac2mp3.py                        8             13             18
-------------------------------------------------------------------------------
SUM:                               133            235            273
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                           7            133            235            273
-------------------------------------------------------------------------------
SUM:                             7            133            235            273
-------------------------------------------------------------------------------
```

* SLOCCount

```sh
SLOC	Directory	SLOC-by-Language (Sorted)
273     top_dir     python=273

Totals grouped by language (dominant language first):
python:         273 (100.00%)

Total Physical Source Lines of Code (SLOC)                = 273
Development Effort Estimate, Person-Years (Person-Months) = 0.05 (0.61)
 (Basic COCOMO model, Person-Months = 2.4 * (KSLOC**1.05))
Schedule Estimate, Years (Months)                         = 0.17 (2.08)
 (Basic COCOMO model, Months = 2.5 * (person-months**0.38))
Estimated Average Number of Developers (Effort/Schedule)  = 0.30
Total Estimated Cost to Develop                           = $ 2,648
 (average salary = $86,261/year, overhead = 0.60).
 
Generated using David A. Wheeler's 'SLOCCount'.
```

## License

Copyright © 2012-2016 Eduardo Ferreira

The code in this repository is MIT licensed, and therefore free to use as you
please for commercial or non-commercial purposes (see [LICENSE](LICENSE) for
details).
