from mserver.application import celery
from mserver.player import playlist
from mserver.socket_server import decorators

_add_song_decorated = decorators.emit_socket_error('player.song_add_error')(playlist.add)
_just_download_song_decorated = decorators.emit_socket_error('player.song_download_error')(playlist.just_download)

song_add = celery.task(_add_song_decorated)
song_just_download = celery.task(_just_download_song_decorated)
