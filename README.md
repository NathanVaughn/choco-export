# About

[Chocolately](https://chocolatey.org/) is a great tool for Windows, but does
not provide any way to export a list of installed packages which then can be
imported on other computers without using
[ChocolatelyGUI](https://github.com/chocolatey/ChocolateyGUI). The GUI also
does not support exporting a list without version numbers, or
exporting a list of enabled Windows features.
This program is an attempt to fill that gap.

# Requirements

Python 3.3+ is required. There are no requirements, but `colorama` can
optionally be installed for colored output messages.

Chocolately also needs to be accessible as `choco` from the command line.

# Usage

## Export

```
usage: export.py [-h] [-dl] [-lo LOCAL_OUTPUT] [-p] [-w] [-wo WINDOWS_OUTPUT]
                 [-v]

Package list exporter for Chocolately

optional arguments:
  -h, --help            show this help message and exit
  -dl, --disable-local  disables exporting a list of locally installed
                        packages (default: False)
  -lo LOCAL_OUTPUT, --local-output LOCAL_OUTPUT
                        path to locally installed packages output file
                        (default: local_packages.config)
  -p, --preserve-versions
                        save the versions of the locally installed packages
                        (default: False)
  -w, --windows-features
                        export a list of enabled Windows features. Program
                        needs to be run with Administrator privileges in order
                        for this to work (default: False)
  -wo WINDOWS_OUTPUT, --windows-output WINDOWS_OUTPUT
                        path to windows features output file (default:
                        windows_features.config)
  -v, --verbose         output more detailed messages (default: False)
```

### Examples

`export.py`

Will output a list of locally installed packages with no versions to
`local_packages.config`

`export.py -p -lo Packages.config`

Will output a list of locally installed packages with versions to
`Packages.config`

`export.py -w`

Will output a list of locally installed packages with no versions to
`local_packages.config` and a list of enabled Windows features to
`windows_features.config`

## Import

### Locally Installed Packages

To install the exported locally installed packages, just run
`choco install ".\local_packages.config"`

### Windows Features

Due to a [bug with chocolatey](https://github.com/chocolatey/choco/issues/877),
you need to install Windows features from a separate file:

`choco install ".\windows_features.config" -s windowsfeatures`

However, Chocolately seems to enable every feature, even if it's already
enabled which is very slow. To help with this, you can use the `compare.py`
program, which takes an input file of Windows features, compares it against
the currently enabled features, and outputs a new XML file of the difference.

Example:

`compare.py windows_features.config -o new_features.config`