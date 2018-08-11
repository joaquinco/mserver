import eventlet

eventlet.monkey_patch()

from mserver.application import app, run_server
from mserver.socket_server.mpd_handlers import listen_mpd

__all__ = ['app', 'listen_mpd', 'run_server']

if __name__ == '__main__':
    run_server()
