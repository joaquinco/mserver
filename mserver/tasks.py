from mserver.application import celery
from mserver.player import playlist

song_add = celery.task(playlist.add)
song_just_download = celery.task(playlist.just_download)
