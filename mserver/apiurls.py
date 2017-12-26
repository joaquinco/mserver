from mserver import resources
from mserver.mserver import api


urls = [
    (resources.SongResource, '/song'),
    (resources.SongDetailResource, '/song/<song_id>'),
    (resources.SongSearchResource, '/search')
]

for url in urls:
    api.add_resource(*url)