from flask import request
from flask_jwt import current_identity
from flask_jwt import jwt_required
from flask_socketio import emit, send

from mserver.mserver import socketio
from mserver.player import playlist
from .utils import start_background_task


@socketio.on('message')
def handle_message(message):
    send(message)


@socketio.on('connect')
@jwt_required()
def on_connect():
    if current_identity:
        emit('user.joined', {'message': '{} connected'.format(current_identity.username)}, broadcast=True)
    else:
        return False
    # emit('user.joined', {'message': 'User connected'}, broadcast=True)


@socketio.on('disconnect')
@jwt_required()
def on_disconnect():
    emit('user.left', {'message': '{} disconnected'.format(current_identity.username)}, broadcast=True)


@socketio.on('player.play')
@jwt_required()
def on_music_play(data):
    """
    Starts playing music.
    Broadcast player state
    """
    emit('player.play', broadcast=True)


@socketio.on('player.pause')
def on_music_paused(data):
    """
    Stops playing music.
    Broadcast player state
    """
    emit('player.pause', broadcast=True)


@socketio.on('player.add_song')
@jwt_required()
def add_song_to_playlist(data):
    source = data.get('source')
    search_id = data.get('search_id')
    playlist_id = data.get('playlist')

    user_id = current_identity.id

    start_background_task(playlist.add, source, search_id, user_id, playlist_id=playlist_id)


@socketio.on_error()
def error_handler(e):
    print('Error encountered ' + str(e))