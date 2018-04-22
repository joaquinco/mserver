import warnings

from flask_restful import marshal

from mserver.database import db
from mserver.marshals import playlist_song_marshal, song_list_marshal
from mserver.models import PlayList, Song
from mserver.mserver import socketio
from mserver.player import search, decorators


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


@decorators.emit_socket_error('player.download_song_error')
def just_download(source, search_id, user_id):
    """
    Just download a song
    """
    _download_song(source, search_id, user_id)


def _download_song(source, search_id, user_id):
    """
    Downloads a song if it's not available or being downloaded
    """
    backend = search.get(source)

    song = backend.get_song(search_id)

    session = song.query.session

    if not song.id:
        song.user_id = user_id
        session.commit()
    elif song.available:
        return song

    socketio.emit('player.song_downloading', marshal(song, song_list_marshal))
    filename = backend.get_file(search_id)

    song.path = filename
    song.available = True
    session.commit()

    socketio.emit('player.song_available', marshal(song, song_list_marshal))

    return song


@decorators.emit_socket_error('player.song_add_error')
def old_add(source, search_id, user_id, playlist_id=None):
    """
    Adds a song to playlist
    """
    warnings.warn("deprecated", DeprecationWarning)
    backend = search.get(source)

    song = backend.get_song(search_id)

    playlist = get_playlist(playlist_id)

    if not song.id:
        song.user_id = user_id
        db.session.add(song)
        db.session.commit()

    playlist.songs.append(song)
    db.session.add(playlist)
    db.session.commit()

    socketio.emit('player.song_added', marshal(dict(song=song, playlist=playlist), playlist_song_marshal))

    if song.available:
        return

    socketio.emit('player.song_downloading', marshal(song, song_list_marshal))
    filename = backend.get_file(search_id)

    song.path = filename

    db.session.query(Song).filter_by(id=song.id).update({"path": filename, "available": True})
    db.session.commit()

    song = Song.query.filter_by(id=song.id).one()

    socketio.emit('player.song_available', marshal(dict(song=song, playlist=playlist), playlist_song_marshal))


@decorators.emit_socket_error('player.song_add_error')
def add(source, search_id, user_id, playlist_id=None):
    """
    Adds a song to playlist
    """
    song = _download_song(source, search_id, user_id)

    playlist = get_playlist(playlist_id)

    playlist.songs.append(song)
    db.session.add(playlist)
    db.session.commit()

    socketio.emit('player.song_added', marshal(dict(song=song, playlist=playlist), playlist_song_marshal))
