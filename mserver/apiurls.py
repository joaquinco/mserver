from mserver import resources
from mserver import api


urls = [
    (resources.SongResource, '/song'),
    (resources.SongDetailResource, '/song/<song_id>')
]

for url in urls:
    api.add_resource(*url)