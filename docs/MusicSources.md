# Music sources

Music can be taken from several sources, but its ultimately always
played by MPD.

## Default Source

Default source is local, which reads from MPD directly.

## Youtube Source

Search and download music from youtube. Uses _youtube-dl_ to download
and convert files, which requires avconv or ffmpeg to be installed
locally.

In debian based, you can installed them by using:

```
apt-get install ffmpeg libav-tools
```