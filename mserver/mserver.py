from flask import Flask

from flask_restful import Api


def create_app():
    app = Flask(__name__)
    app.config.from_object('mserver.settings')

    return app


def create_api(app=None):
    api = Api(app or create_app())
    return api


app = create_app()
api = create_api(app)


def do_setup():
    from .database import init_db
    init_db()


do_setup()