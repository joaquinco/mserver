from flask_restful import marshal

from mserver.database import db
from mserver.marshals import playlist_song_marshal
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


@decorators.handle_exception('player.song_add_error')
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

    socketio.emit('player.song_added', marshal(dict(song=song, playlist=playlist), playlist_song_marshal))

    if song.available:
        return

    filename = backend.get_file(search_id)

    song.path = filename

    db.session.query(Song).filter_by(id=song.id).update({"path": filename, "available": True})
    db.session.commit()

    song = Song.query.filter_by(id=song.id).one()

    socketio.emit('player.song_available', marshal(dict(song=song, playlist=playlist), playlist_song_marshal))
