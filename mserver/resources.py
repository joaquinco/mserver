from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy.orm.exc import NoResultFound

from mserver.player import search
from .models import Song

song_list_marshal = {
    'id': fields.Integer,
    'title': fields.String,
    'artist': fields.String,
    'album': fields.String,
    'duration': fields.String
}

song_search_marshal = {
    'search_id': fields.String,
    'title': fields.String,
    'duration': fields.String
}


class SongResource(Resource):
    @marshal_with(song_list_marshal)
    def get(self):
        return Song.query.all()

    @marshal_with(song_list_marshal)
    def create(self):
        raise NotImplementedError('SongResource.create')

    post = put = create


search_args = reqparse.RequestParser()
search_args.add_argument('query', help='Search query', required=True, location='args')
search_args.add_argument('source', required=False, location='args')


class SongSearchResource(Resource):
    @marshal_with(song_search_marshal)
    def get(self):
        args = search_args.parse_args()
        query = args.get('query')
        source = args.get('source')

        if source:
            backend = search.get(source)
        else:
            backend = search.get_default()

        return backend.search(query)


class SongDetailResource(Resource):
    @marshal_with(song_list_marshal)
    def get(self, song_id):
        try:
            return Song.query.filter(id=song_id).one()
        except NoResultFound:
            abort(404)
