from functools import partial

from mserver import mpd_utils
from mserver.application import socketio
from mserver.socket_server.handlers import emit_player_status, emit_player_currentsong
from mserver.socket_server.utils import emit


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

    mpd_utils.listen_events(mpd_event_handlers.keys(), callback)
