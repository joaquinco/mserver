from functools import partial
from threading import Thread

from flask_jwt import current_identity
from flask_jwt import jwt_required

from mserver import mpd
from mserver.mserver import socketio
from mserver.player import playlist
from .utils import start_background_task, emit


def on_connect():
    if current_identity:
        emit('user.joined', {'message': '{} connected'.format(current_identity.username)}, broadcast=True)
    else:
        return False


def on_disconnect():
    emit('user.left', {'message': '{} disconnected'.format(current_identity.username)}, broadcast=True)


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


def emit_player_status(broadcast=False):
    emit('player.status', mpd.status(), broadcast=broadcast)


def emit_player_currentsong(broadcast=False):
    emit('player.current', playlist.get_current_song_marshaled(), broadcast=broadcast)


def mpd_write_command_wrapper(command_name, data_key=None):
    fn = getattr(mpd, command_name)

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

    # Player dummy write actions
    ('player.next', True, mpd_write_command_wrapper('next')),
    ('player.previous', True, mpd_write_command_wrapper('previous')),
    ('player.play', True, mpd_write_command_wrapper('play')),
    ('player.pause', True, mpd_write_command_wrapper('pause')),
    ('player.random', True, mpd_write_command_wrapper('random', 'value')),
    ('player.repeat', True, mpd_write_command_wrapper('repeat', 'value')),
    ('player.select', True, mpd_write_command_wrapper('play', 'pos')),
    ('player.remove', True, mpd_write_command_wrapper('delete', 'pos')),

    # Other more complex
    ('player.add_song', True, add_song_to_playlist),
    ('player.download_song', True, just_download_song),
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


def emit_full_player_state(broadcast=False):
    emit_player_status(broadcast=broadcast)
    emit_player_currentsong(broadcast=broadcast)


def emit_playlist_changed(broadcast=True):
    emit('player.playlist_changed', broadcast=broadcast)


mpd_event_handlers = {
    'player': partial(emit_full_player_state, broadcast=True),
    'playlist': emit_playlist_changed,
    'mixer': partial(emit_player_status, broadcast=True),
    'options': partial(emit_player_status, broadcast=True)
}


def listen_mpd():
    def callback(event):
        mpd_event_handlers.get(event)()

    thread = Thread(target=mpd.listen_events, args=(mpd_event_handlers.keys(), callback))

    thread.daemon = True
    thread.start()


# TODO: put elsewhere
listen_mpd()
