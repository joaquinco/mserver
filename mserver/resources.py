from flask import request
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, marshal_with, reqparse

from mserver import rpc
from mserver.marshals import song_search_marshal, playlist_detail_marshal, user_detail_marshal
from mserver.player import search, playlist

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

        playlist.add(source, search_id, user.id, playlist_id)

        return {}, 204

    @marshal_with(playlist_detail_marshal)
    @jwt_required()
    def get(self, playlist_id=None):
        return playlist.get_playlist(playlist_id)
        # TODO: should list if playlist_id==None else detail


rpc_post_params = reqparse.RequestParser()
rpc_post_params.add_argument('args', help='argument list', required=False, location='json', default=lambda: [],
                             type=list)
rpc_post_params.add_argument('kwargs', required=False, location='json', default=lambda: {}, type=dict)


class RPCResource(Resource):
    def __init__(self, *args, **kwargs):
        self.post = self.get = self.call_rpc
        super().__init__(*args, **kwargs)

    def get(self, rpc_name):
        return self.call_rpc(rpc_name, **request.args)

    def post(self, rpc_name):
        args = rpc_post_params.parse_args()
        return self.call_rpc(rpc_name, *args.get('args', []), **args.get('kwargs', {}))

    def call_rpc(self, rpc_name, *args, **kwargs):
        return rpc.call(rpc_name, *args, **kwargs)


class UserResource(Resource):
    @marshal_with(user_detail_marshal)
    @jwt_required()
    def get(self):
        return current_identity
