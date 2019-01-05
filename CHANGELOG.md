## History

Version 0.0.4

*
*
*

Version 0.0.3

* Added input parameter validation for the methods in the interface module
* Added unit tests for the interface module
* Created a package for the library modules
* Created a package for the unit tests
* Reset the input parameters for the various scripts
  * Kept the input and output parameters
  * Removed all the remaining parameters (related to ID3 tags, album cover art and playlists)

Version 0.0.2

* Added input parameter validation for the methods in the audio library
* Added external dependency validation for the following programs:
  * lame
  * flac
  * metaflac
  * grep
  * sed

Version 0.0.1

* Reset the version number to 0.0.1
* Changed app name to Anarky
* Added a logger
* Reviewed the method headers to add parameter and return descriptions
* Small refactoring to group tightly coupled code in the same Python files
* Made sure that all workflows are working without any tag, cover and playlist management

## Versioning

This application will be maintained under the Semantic Versioning guidelines as much as possible.

Releases will be numbered with the following format:

`<major>.<minor>.<patch>`

And constructed with the following guidelines:

* Breaking backward compatibility bumps the major (and resets the minor and patch)
* New additions without breaking backward compatibility bumps the minor (and resets the patch)
* Bug fixes and misc changes bumps the patch

For more information on SemVer, please visit [http://semver.org/](http://semver.org/).
