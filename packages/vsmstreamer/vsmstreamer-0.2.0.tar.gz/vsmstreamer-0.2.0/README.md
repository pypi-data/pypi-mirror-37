# Cisco Video Surveillance Manager Streamer

[![PyPI version](https://badge.fury.io/py/vsmstreamer.svg)](https://badge.fury.io/py/vsmstreamer)

*vsmstreamer* is a Python utility to stream Cisco Video Surveillance Manager
streams on macOS.

## Requirements

This utility requires the following software:

  - macOS (tested using 18.0.0, Mojave)
  - Python 2.7 or 3 (tested using 2.7.15, and 3.7)
  - [VLC media player Nightly Build](https://nightlies.videolan.org/build/macosx-intel/) (tested using vlc-3.0.5-20181022-0636)

**Note:** Due to a bug in VLC 3.0.4, you MUST use a nightly build of 3.0.5.
Otherwise, the stream will stop after 120 second. For more information read
[this thread](https://forum.videolan.org/viewtopic.php?f=12&t=146754).
  
These are the Python modules that the utility depends on:

  - [configparser](https://pypi.org/project/configparser/)
  - [requests](https://github.com/requests/requests.git)
  - [PyCocoa](https://github.com/mrJean1/PyCocoa)
  - [python-vlc](https://pypi.org/project/python-vlc/)
  
However, you need not install these packages by hand. Installing *vsmstreamer*
through `pip` will automatically install these packages.
  
## Installation

### From PyPI

The latest released version of *vsmstreamer* can be installed from
[PyPI](https://pypi.org/project/vsmstreamer/).

```
pip install vsmstreamer
```

PS: Run with `sudo` like `sudo pip install vsmstreamer` if necessary.

### From Source

The latest development version of *vstreamer* can be installed from source.

```
git clone https://github.com/kprav33n/vsmstreamer.git
pip install -e ./vsmstreamer
```

## Usage

`vsmstreamer` is a command line utility. The following summarizes list of
options available.

```
$ vsmstreamer --help
usage: vsmstreamer [-h] [--config CONFIG] [--profile PROFILE]
                   [--server SERVER] [--username USERNAME]
                   [--password PASSWORD] [--stream STREAM]

Cisco Video Surveillance Manager Streamer

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        path to config file
  --profile PROFILE, -r PROFILE
                        profile name to use
  --server SERVER, -s SERVER
                        VSM server address
  --username USERNAME, -u USERNAME
                        VSM username
  --password PASSWORD, -p PASSWORD
                        VSM password
  --stream STREAM, -n STREAM
                        stream index to display
```

In order to stream from a Cisco Video Surveillance Manager, you would need the
following three parameters:

  - server address
  - username
  - password
  
### Credentials File

The above mentioned parameters can be stored in a credentials file. The default
path of the credentials file is `~/.vsm/credentials`. However, this path can be
overridden using the `--config` command line option. This file can contain one
are more sections. The section name is enclosed in a square bracket like this
`[default]`. A desired section can be selected using the `--profile` command
line option. A sample credentials file looks like this:

```
[default]
server = vsm.example.org
username = jsmith
password = $up3rsecret
```

However, use of credentials file is optional. In the absence of the credentials
file, the command line options `--server`, `--user`, and `--password` can be
used to specify the required parameters.

### Streams

*vsmstreamer* plays only one stream at a time. You can have many instances of
this utility running at the same time if you want to want multiple streams. By
default, this utility tunes to the first stream in the list of available
streams. However, you can use `--stream` command line option to specify the
stream index (0-indexed) to tune into.

## Feedback

If you find a bug, or you would like to see a new feature, please feel free to
[open an issue](https://github.com/kprav33n/vsmstreamer/issues).
