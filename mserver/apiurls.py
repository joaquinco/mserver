from urllib import parse as urlparse

from mserver import resources
from mserver.mserver import api

API_PREFIX = '/api/'

urls = [
    (resources.SongSearchResource, 'search')
]

for resource, path in urls:
    api.add_resource(resource, urlparse.urljoin(API_PREFIX, path))
