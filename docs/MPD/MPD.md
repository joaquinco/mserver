## MPD

The version utilized is 0.20.20

Full documentation can be found here: https://www.musicpd.org/doc/user/

### Instalation

1. Download version's source code from http://www.musicpd.org
2. Install build dependencies: `build-essential libboost-dev`
3. `./configure`
4. `make`
5. `sudo make install`

### Basic Running

`mpd mpd.conf`

### Recommended configuration


- music_directory: final path from where music is played
- database: mpd database configuration
- input: audio configuration