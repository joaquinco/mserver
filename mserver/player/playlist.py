import os

from mserver.mserver import db
from mserver.models import PlayList, Song
from mserver.player import search


def get_playlist(playlist_id=None):
    """
    Gets playlist. If playlist is None return default.
    """
    if playlist_id:
        playlist = PlayList.query.filter_by(id=playlist_id).one()
    else:
        playlist = PlayList.query.filter_by(is_default=True).first()
        if not playlist:
            playlist = PlayList(name='default', is_default=True)
            db.session.add(playlist)
            db.session.commit()
    return playlist


def add(source, search_id, user_id, playlist_id=None):
    """
    Adds a song to playlist
    """
    if source:
        backend = search.get(source)
    else:
        backend = search.get_default()

    song = backend.get_song(search_id)

    playlist = get_playlist(playlist_id)

    if not song.id:
        song.user_id = user_id
        db.session.add(song)
        db.session.commit()

    playlist.songs.append(song)
    db.session.add(playlist)
    db.session.commit()

    if playlist.is_playing:
        # TODO: broadcast added song
        pass

    if song.available:
        return

    filename = backend.get_file(search_id)

    song.path = filename

    db.session.query(Song).filter_by(id=song.id).update({"path": filename, "available": True})
    db.session.commit()

    # TODO: broadcast song is available


