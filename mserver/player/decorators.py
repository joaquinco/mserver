import logging
import traceback

from flask_socketio import emit

from .exceptions import MServerException


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
                emit('error', {'message': str(e), 'key': error_key, 'detail': context})

        return wrapper

    return decorator
