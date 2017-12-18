from flask_restful import Resource, fields, marshal_with, abort
from sqlalchemy.orm.exc import NoResultFound

from .models import Song

song_list_marshal = {
    'id': fields.Integer,
    'name': fields.String,
    'artist': fields.String,
    'album': fields.String
}


class SongResource(Resource):
    @marshal_with(song_list_marshal)
    def get(self):
        return Song.query.all()

    @marshal_with(song_list_marshal)
    def create(self):
        raise NotImplementedError('SongResource.create')

    post = put = create


class SongDetailResource(Resource):
    @marshal_with(song_list_marshal)
    def get(self, song_id):
        try:
            return Song.query.filter(id=song_id).one()
        except NoResultFound:
            abort(404)
