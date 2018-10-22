from flask import request
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, marshal_with, reqparse

from mserver import rpc, auth, music_sources
from mserver.marshals import song_search_marshal, user_detail_marshal, dummy_song_playlist_list_marshal
from mserver.player import playlist

search_args = reqparse.RequestParser()
search_args.add_argument('query', help='Search query', required=True, location='args')
search_args.add_argument('source', required=False, location='args')


class SongSearchResource(Resource):
    @marshal_with(song_search_marshal)
    # @jwt_required()
    def get(self):
        args = search_args.parse_args()
        query = args.get('query')
        source = args.get('source')

        backend = music_sources.get(source)

        return backend.search(query)


class PlaylistResource(Resource):
    @marshal_with(dummy_song_playlist_list_marshal)
    @jwt_required()
    def get(self):
        return playlist.list_playlist_songs()


addsong_args = reqparse.RequestParser()
addsong_args.add_argument('search_id', help='Search id', required=True, location='json')
addsong_args.add_argument('source', required=False, location='json')

rpc_post_params = reqparse.RequestParser()
rpc_post_params.add_argument('args', help='argument list', required=False, location='json', default=lambda: [],
                             type=list)
rpc_post_params.add_argument('kwargs', required=False, location='json', default=lambda: {}, type=dict)


class RPCResource(Resource):
    def get(self, rpc_name):
        return self.call_rpc(rpc_name, **request.args)

    def post(self, rpc_name):
        args = rpc_post_params.parse_args()
        return self.call_rpc(rpc_name, *args.get('args', []), **args.get('kwargs', {}))

    def call_rpc(self, rpc_name, *args, **kwargs):
        return rpc.call(rpc_name, *args, **kwargs)


class SecureRPCResource(RPCResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get = jwt_required()(self.get)
        self.post = jwt_required()(self.post)

    def call_rpc(self, rpc_name, *args, **kwargs):
        return rpc.call(rpc_name, *args, secure=True, **kwargs)


class AuthResource(Resource):
    @marshal_with(user_detail_marshal)
    @jwt_required()
    def get(self):
        return current_identity

    def post(self):
        return auth.auth_request_handler()
