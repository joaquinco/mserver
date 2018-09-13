from functools import partial

from flask_jwt import current_identity
from flask_jwt import jwt_required

from mserver import mpd_utils, tasks
from mserver.application import socketio
from mserver.player import playlist
from mserver.socket_server.utils import emit


def on_connect():
    if current_identity:
        emit('user.joined', {'message': '{} connected'.format(current_identity.username)}, broadcast=True)
    else:
        return False


def on_disconnect():
    emit('user.left', {'message': '{} disconnected'.format(current_identity.username)}, broadcast=True)


def add_song_to_playlist(data, play_next=False):
    source = data.get('source')
    search_id = data.get('search_id')

    user_id = current_identity.id

    tasks.song_add.delay(source, search_id, user_id, play_next)


add_next_song_to_playlist = partial(add_song_to_playlist, play_next=True)


def just_download_song(data):
    source = data.get('source')
    search_id = data.get('search_id')

    user_id = current_identity.id

    tasks.song_just_download.delay(source, search_id, user_id)


def emit_player_status(broadcast=False):
    emit('player.status', mpd_utils.status(), broadcast=broadcast)


def emit_player_currentsong(broadcast=False):
    emit('player.current', playlist.get_current_song_marshaled(), broadcast=broadcast)


def mpd_write_command_wrapper(command_name, data_key=None):
    fn = getattr(mpd_utils, command_name)

    def wrapped(data=None):
        params = ()
        if data_key is not None:
            if data_key == '__all__':
                value = data
            else:
                value = data.get(data_key)
            params = (value,)
        return fn(*params)

    return wrapped


events = [
    ('connect', True, on_connect),
    ('disconnect', True, on_disconnect),

    # Player read actions
    ('player.status', True, emit_player_status),
    ('player.current', True, emit_player_currentsong),

    # Player simple write actions
    ('player.next', True, mpd_write_command_wrapper('next')),
    ('player.previous', True, mpd_write_command_wrapper('previous')),
    ('player.play', True, mpd_write_command_wrapper('play')),
    ('player.pause', True, mpd_write_command_wrapper('pause')),
    ('player.random', True, mpd_write_command_wrapper('random', 'value')),
    ('player.repeat', True, mpd_write_command_wrapper('repeat', 'value')),
    ('player.select', True, mpd_write_command_wrapper('play', 'pos')),
    ('player.remove', True, mpd_write_command_wrapper('delete', 'pos')),
    ('player.volume', True, mpd_write_command_wrapper('setvol', 'value')),

    # Other more complex
    ('player.add_song', True, add_song_to_playlist),
    ('player.add_song_next', True, add_next_song_to_playlist),
    ('player.download_song', True, just_download_song),
]


def _setup_events():
    global events
    for event_name, requires_auth, handler in events:
        method = requires_auth and jwt_required()(handler) or handler
        socketio.on(event_name)(method)


_setup_events()
