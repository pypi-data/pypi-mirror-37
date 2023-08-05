# m3ushuffler

*Shuffle your M3U Playlists easily!*

This simple python tool will shuffle your M3U playlists while keeping the
Extended M3U (EXTM3U) metadata in the right place. If you want to
shuffle M3U playlists without metadata (i.e. without files starting with
`#EXTINF`), you can simply use `shuf` instead:

    shuf /path/to/playlist.m3u > /path/to/output.m3u


## Installation

You can install it via `pip`/`pip3`:

    $ pip3 install --user m3ushuffler

As an alternative, you can install it directly from source:

    $ git clone https://github.com/Holzhaus/m3ushuffler.git
    $ cd m3ushuffler
    $ ./setup.py install --user


## Usage

    $ m3ushuffler -h
    usage: m3ushuffler [-h] [-o OUTPUT_FILE] [-d] input_file
    
    positional arguments:
      input_file            The M3U playlist to randomize
    
    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT_FILE, --output-file OUTPUT_FILE
                            The M3U output file to write to
      -d, --debug           Show debug messages


## License

See [LICENSE](LICENSE).
