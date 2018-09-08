from mserver.application import app, run_server
from mserver.socket_server.mpd_handlers import listen_mpd

name = 'mserver'

__all__ = ['app', 'listen_mpd', 'run_server']
