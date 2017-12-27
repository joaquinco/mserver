import os

from mserver.player import search


def get_playlist(playlist_id=None):
    """
    Gets playlist. If playlist is None return default.
    """


def add(source, search_id, playlist_id=None):
    """
    Adds a song to playlist
    """
    if source:
        backend = search.get(source)
    else:
        backend = search.get_default()

    song = backend.get_song(search_id)

    playlist = get_playlist(playlist_id)

    if playlist.is_playing:
        # TODO: broadcast added song
        pass

    if not song.available:


    # TODO: add song to playlist

    if song.available:
        return

    filename = backend.get_file(search_id)

    basename = os.path.basename(filename)

    song.path
