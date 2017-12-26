from mserver import resources
from mserver.mserver import api

API_PREFIX = '/api/'

urls = [
    (resources.SongSearchResource, 'search'),
    (resources.PlayListResource, 'playlist/<int:playlist_id>', 'playlist')
]


def join_path(prefix, path):
    return '/{}'.format('/'.join([s.strip('/') for s in [prefix, path]]))


for params in urls:
    resource = params[0]
    paths = params[1:]
    api.add_resource(resource, *[join_path(API_PREFIX, path) for path in paths])
