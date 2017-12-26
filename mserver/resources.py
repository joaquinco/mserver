from flask_restful import Resource, fields, marshal_with, reqparse

from mserver.player import search

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
    def get(self):
        args = search_args.parse_args()
        query = args.get('query')
        source = args.get('source')

        if source:
            backend = search.get(source)
        else:
            backend = search.get_default()

        return backend.search(query)
