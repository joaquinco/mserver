from flask_restful import marshal

from mserver import mpd_utils
from mserver.database import db
from mserver.marshals import song_list_marshal, dummy_song_playlist_list_marshal
from mserver.application import socketio
from mserver.player import search
from mserver.player.utils import mpd_convert_to_song


def just_download(source, search_id, user_id):
    """
    Just download a song
    """
    song = _get_song(source, search_id, user_id)

    socketio.emit('player.song_available', marshal(song, song_list_marshal))


def _get_song(source, search_id, user_id):
    """
    Downloads a song if it's not available or being downloaded
    """
    backend = search.get(source)

    song = backend.get_song(search_id)

    if not song.id:
        song.user_id = user_id
        song.downloading = True
        db.session.add(song)
        db.session.commit()
    elif song.available:
        return song

    raise_exception = None

    try:
        socketio.emit('player.song_downloading', marshal(song, song_list_marshal))
        filename = backend.get_file(search_id)

        song.path = filename

        mpd_utils.update(filename)
    except Exception as e:
        song.downloading = False
        song.error = str(e)
        raise_exception = e
    else:
        song.downloading = False
        song.available = True

    db.session.add(song)
    db.session.commit()

    if raise_exception:
        raise raise_exception

    return song


def add(source, search_id, user_id):
    """
    Adds a song to playlist
    """
    song = _get_song(source, search_id, user_id)

    print(song.path)
    mpd_utils.add(song.path)

    socketio.emit('player.song_added', marshal(song, song_list_marshal))


def list_playlist_songs(playlist=None):
    """
    Returns list of Song objects
    """
    return list(map(mpd_convert_to_song, mpd_utils.playlist()))


def get_current_song():
    """
    Returns current song
    """
    return mpd_convert_to_song(mpd_utils.currentsong())


def get_current_song_marshaled():
    return marshal(get_current_song(), dummy_song_playlist_list_marshal)
