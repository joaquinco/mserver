from flask_restful import marshal

from mserver.database import db
from mserver.marshals import song_list_marshal, dummy_song_playlist_list_marshal
from mserver.models import Song
from mserver.mserver import socketio
from mserver.player import mpd
from mserver.player import search, decorators
from mserver.player.utils import mpd_convert_to_song


@decorators.emit_socket_error('player.song_download_error')
def just_download(source, search_id, user_id):
    """
    Just download a song
    """
    _get_song(source, search_id, user_id)


def _download_song_tmp(source, search_id, user_id):
    # socketio = get_socketio()
    backend = search.get(source)

    song = backend.get_song(search_id)

    socketio.emit('player.song_downloading', marshal(song, song_list_marshal))

    import time
    time.sleep(10)

    # filename = backend.get_file(search_id)

    socketio.emit('player.song_available', marshal(song, song_list_marshal), broadcast=True)


def _get_song(source, search_id, user_id):
    """
    Downloads a song if it's not available or being downloaded
    """
    # socketio = get_socketio()
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

    print(filename)

    mpd.mpd_add_song_to_db(filename)

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
    # socketio = get_socketio()
    song = _get_song(source, search_id, user_id)

    mpd.mpd_add_song(song.title)

    socketio.emit('player.song_added', marshal(song, song_list_marshal), broadcast=True)


def list_playlist_songs(playlist=None):
    """
    Returns list of Song objects
    """
    return list(map(mpd_convert_to_song, mpd.mpd_get_playlist()))


def get_current_song():
    """
    Returns current song
    """
    return mpd_convert_to_song(mpd.mpd_get_current())


def get_current_song_marshaled():
    return marshal(get_current_song(), dummy_song_playlist_list_marshal)
