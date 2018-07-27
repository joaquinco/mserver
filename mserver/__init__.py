import eventlet

eventlet.monkey_patch()

from .application import app, run_server

__all__ = ['app']

if __name__ == '__main__':
    run_server()
