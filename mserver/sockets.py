from flask_jwt import current_identity
from flask_socketio import emit

from mserver.mserver import socketio

music_player = '/player'


@socketio.on('connect', namespace=music_player)
def on_connect():
    # if current_identity:
    #     emit('user.joined', {'message': '{} connected'.format(current_identity.username)})
    # else:
    #     return False
    emit('user.joined', {'message': 'User connected'})


@socketio.on('disconnect', namespace=music_player)
def on_disconnect():
    emit('user.joined', {'message': '{} connected'.format(current_identity.username)})


@socketio.on('play', namespace=music_player)
def on_music_play(data):
    """
    Starts playing music.
    Broadcast player state
    """
    print('Play button clicked')


@socketio.on('pause', namespace=music_player)
def on_music_paused(data):
    """
    Stops playing music.
    Broadcast player state
    """
    print('Pause button clicked')
