import logging
import traceback

from mserver.application import socketio
from mserver.exceptions import MServerException


def emit_socket_error(error_key):
    """
    Calls method and emit proper error on exception.

    Meant to be used by socket handlers.
    """

    def decorator(wrapped):
        def wrapper(*args, **kwargs):
            try:
                return wrapped(*args, **kwargs)
            except Exception as e:
                logging.error('Socket error: %s', traceback.print_exc())
                context = {}
                if isinstance(e, MServerException):
                    context = e.context
                socketio.emit(error_key, {'message': str(e), 'detail': context})

        wrapper.__name__ = wrapped.__name__

        return wrapper
    return decorator
