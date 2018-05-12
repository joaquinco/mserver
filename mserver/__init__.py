import eventlet

eventlet.monkey_patch()

from .mserver import app

__all__ = ['app']
