import warnings

from flask_restful import marshal

from mserver.database import db
from mserver.marshals import playlist_song_marshal, song_list_marshal
from mserver.models import PlayList, Song
from mserver.player import search, decorators
from mserver.mserver import get_socketio


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


@decorators.emit_socket_error('player.song_download_error')
def just_download(source, search_id, user_id):
    """
    Just download a song
    """
    _download_song(source, search_id, user_id)


def _download_song_tmp(source, search_id, user_id):
    socketio = get_socketio()
    backend = search.get(source)

    song = backend.get_song(search_id)

    socketio('player.song_downloading', marshal(song, song_list_marshal))

    import time
    time.sleep(10)

    # filename = backend.get_file(search_id)

    socketio('player.song_available', marshal(song, song_list_marshal), broadcast=True)


def _download_song(source, search_id, user_id):
    """
    Downloads a song if it's not available or being downloaded
    """
    socketio = get_socketio()
    backend = search.get(source)

    song = backend.get_song(search_id)

    if not song.id:
        song.user_id = user_id
        db.session.add(song)
        db.session.commit()
    elif song.available:
        return song

    socketio.emit('player.song_downloading', marshal(song, song_list_marshal))
    filename = backend.get_file(search_id)

    song = db.session.query(Song).filter_by(id=song.id).scalar()

    song.path = filename
    song.available = True
    db.session.add(song)
    db.session.commit()

    socketio.emit('player.song_available', marshal(song, song_list_marshal), broadcast=False)

    return song


@decorators.emit_socket_error('player.song_add_error')
def add(source, search_id, user_id, playlist_id=None):
    """
    Adds a song to playlist
    """
    socketio = get_socketio()
    song = _download_song(source, search_id, user_id)

    playlist = get_playlist(playlist_id)

    playlist.songs.append(song)
    db.session.add(playlist)
    db.session.commit()

    socketio('player.song_added', marshal(dict(song=song, playlist=playlist), playlist_song_marshal),
                    broadcast=True)
