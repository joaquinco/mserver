from threading import Thread

from flask_jwt import current_identity
from flask_jwt import jwt_required
from flask_socketio import emit

from mserver.mpd.listener import listen_events as mpd_listen_events
from mserver.mserver import socketio
from mserver.player import playlist, mpd
from .utils import start_background_task


def on_connect():
    if current_identity:
        emit('user.joined', {'message': '{} connected'.format(current_identity.username)}, broadcast=True)
    else:
        return False


def on_disconnect():
    emit('user.left', {'message': '{} disconnected'.format(current_identity.username)}, broadcast=True)


def on_music_play(data=None):
    """
    Starts playing music.
    Broadcast player state
    """
    mpd.mpd_play()
    emit('player.play', broadcast=True)
    player_status()


def on_music_paused(data=None):
    """
    Stops playing music.
    Broadcast player state
    """
    mpd.mpd_pause()
    emit('player.pause', broadcast=True)
    player_status()


def add_song_to_playlist(data):
    source = data.get('source')
    search_id = data.get('search_id')
    playlist_id = data.get('playlist')

    user_id = current_identity.id

    start_background_task(playlist.add, source, search_id, user_id, playlist_id=playlist_id)


def just_download_song(data):
    source = data.get('source')
    search_id = data.get('search_id')

    user_id = current_identity.id

    start_background_task(playlist.just_download, source, search_id, user_id)


def player_next(data=None):
    mpd.mpd_next()
    emit('player.next', broadcast=True)
    _emit_player_current(broadcast=True)


def player_previous(data=None):
    mpd.mpd_previous()
    emit('player.previous', broadcast=True)
    _emit_player_current(broadcast=True)


def _emit_player_current(broadcast=False):
    emit('player.current', playlist.get_current_song_marshaled(), broadcast=broadcast)


def player_random(data):
    mpd.mpd_random(data.get('value'))
    player_status()


def player_repeat(data):
    mpd.mpd_repeat(data.get('value'))
    player_status()


def player_status():
    emit('player.status', mpd.mpd_get_status(), broadcast=True)


def player_select_song(song):
    mpd.mpd_select(song.get('pos'))
    _emit_player_current()
    player_status()


def player_remove_song(song):
    pos = song.get('pos')

    if pos is None:
        return

    mpd.mpd_delete(pos)
    emit('player.song_removed', song)


def playlist_changed():
    emit('player.playlist_changed')


events = [
    ('connect', True, on_connect),
    ('disconnect', True, on_disconnect),
    ('player.play', True, on_music_play),
    ('player.pause', True, on_music_paused),
    ('player.add_song', True, add_song_to_playlist),
    ('player.download_song', True, just_download_song),
    ('player.next', True, player_next),
    ('player.previous', True, player_previous),
    ('player.current', True, _emit_player_current),
    ('player.random', True, player_random),
    ('player.repeat', True, player_repeat),
    ('player.status', True, player_status),
    ('player.select', True, player_select_song),
    ('player.remove', True, player_remove_song)
]


def _setup_events():
    global events
    for event_name, requires_auth, handler in events:
        method = requires_auth and jwt_required()(handler) or handler
        socketio.on(event_name)(method)


_setup_events()


@socketio.on_error()
def error_handler(e):
    print('Error encountered ' + str(e))


def player_control_state():
    player_status()
    _emit_player_current()


mpd_event_handlers = {
    'player': player_control_state,
    'playlist': playlist_changed,
    'mixer': player_status,
    'options': player_status
}


def listen_mpd():
    def callback(event):
        mpd_event_handlers.get(event)()

    thread = Thread(target=mpd_listen_events, args=(mpd_event_handlers.keys(), callback))

    thread.daemon = True
    thread.start()


# TODO: put elsewhere
listen_mpd()
