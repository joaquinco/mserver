from flask_socketio import SocketIO

from .database import db_session
from .mserver import api, app


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    SocketIO.run(app)
