from .database import db_session
from .mserver import api, app


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
