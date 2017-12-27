from flask_restful import Resource, fields, marshal_with, reqparse

from mserver.player import search
from flask_jwt import jwt_required, current_identity

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
    'duration': fields.String,
    'available': fields.Boolean,
    'source': fields.String
}

search_args = reqparse.RequestParser()
search_args.add_argument('query', help='Search query', required=True, location='args')
search_args.add_argument('source', required=False, location='args')


class SongSearchResource(Resource):
    @marshal_with(song_search_marshal)
    @jwt_required()
    def get(self):
        args = search_args.parse_args()
        query = args.get('query')
        source = args.get('source')

        if source:
            backend = search.get(source)
        else:
            backend = search.get_default()

        return backend.search(query)


addsong_args = reqparse.RequestParser()
addsong_args.add_argument('search_id', help='Search id', required=True, location='json')
addsong_args.add_argument('source', required=False, location='json')


class PlayListResource(Resource):
    @jwt_required()
    def post(self, playlist_id=None):
        args = addsong_args.parse_args()

        search_id = args.get('search_id')
        source = args.get('source')
        user = current_identity

        if source:
            backend = search.get(source)
        else:
            backend = search.get_default()

        playlist.add()

        return backend.get_file(search_id)
