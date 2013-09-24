## History

Version 0.1.4

* Command line interface is now managed with the `argparse` module
* Simplified the entire audio library
* Dynamically retrieve the artist and album names from the ID3 tags of an audio file to generate a playlist file. In case they are unavailable, the dummy strings "artist" and "album" are used, respectively

Version 0.1.3

* Added three new options ("-c", "-p" and "-t") and updated the old options
* Further generalization of commnand line related methods and migration to the interface library
* Refinement of the audio library

Version 0.1.2

* Removed the "-F" option to supply a directory with input files. This means that the programs only accept lists of files as input for processing with the "-f" option
* Generalized some of the command line related methods and migrated them to a new interface library

Version 0.1.1

* Added the "-h", "-v", "-d", "-f" and "-F" options
* Refactored major portions of the code, mostly by replacing "hand made" code with Python built-in functions

Version 0.1.0

* Initial version

## Versioning

This application will be maintained under the Semantic Versioning guidelines as much as possible.

Releases will be numbered with the following format:

`<major>.<minor>.<patch>`

And constructed with the following guidelines:

* Breaking backward compatibility bumps the major (and resets the minor and patch)
* New additions without breaking backward compatibility bumps the minor (and resets the patch)
* Bug fixes and misc changes bumps the patch

For more information on SemVer, please visit [http://semver.org/](http://semver.org/).
