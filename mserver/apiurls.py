from mserver import resources
from mserver.application import api
from .auth import auth_request_handler

API_PREFIX = '/api/'

urls = [
    (resources.SongSearchResource, 'search'),
    (resources.PlaylistResource, 'playlist'),
    (resources.RPCResource, 'rpc/<string:rpc_name>'),
    (resources.SecureRPCResource, 'srpc/<string:rpc_name>'),
    (resources.AuthResource, 'auth'),
]


def join_path(prefix, path):
    return '/{}'.format('/'.join([s.strip('/') for s in [prefix, path]]))


for params in urls:
    resource = params[0]
    paths = params[1:]
    api.add_resource(resource, *[join_path(API_PREFIX, path) for path in paths])
