from flask_socketio import SocketIO

from .mserver import api, app

if __name__ == '__main__':
    SocketIO.run(app)
