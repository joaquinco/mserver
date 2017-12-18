from flask import Flask

from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = None
app = None
api = None


def create_app():
    app = Flask(__name__)
    app.config.from_object('mserver.settings')

    return app


def create_api(app):
    api = Api(app)
    return api


def do_setup(app):
    from .database import init_db
    init_db()

    # global db
    # db = SQLAlchemy()
    # db.init_app(app)
    import mserver.player.search

    import mserver.resources
    mserver.resources.SongResource


app = create_app()
api = create_api(app)
do_setup(app)
