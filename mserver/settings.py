import datetime
import logging
import os

import dotenv

dotenv.load_dotenv()

DEBUG = True

SECRET_KEY = b'\xd0H\xbdA\xdb`\xa5\x86\xca\x1d\xc2\xd6Z\x89\xa5\x8e\x0e\x0c\x93\xfaDCh\x91C)yh\xe5xxx'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MUSIC_DIR = os.getenv('MSERVER_MUSIC_DIR') or os.path.join(BASE_DIR, 'storage')

LOG_DIR = os.getenv('MSERVER_LOG_DIR') or os.path.join(BASE_DIR, 'log')

LOG_LEVEL = os.getenv('MSERVER_LOG_LEVEL') or 'DEBUG'

LOG_LEVEL = getattr(logging, LOG_LEVEL)

for directory in [MUSIC_DIR, LOG_DIR]:
    if not os.path.exists(directory):
        os.mkdir(directory)

LOGGERS = [
    'mpd', 'mpd_listener', 'celery.task', 'mserver', 'mserver.socketio'
]

JWT_AUTH_URL_RULE = None
JWT_AUTH_ENDPOINT = 'auth'
JWT_AUTH_HEADER_PREFIX = 'Bearer'
JWT_VERIFY_EXPIRATION = False
JWT_EXPIRATION_DELTA = datetime.timedelta(days=365)

SOCKETIO_ASYNC_MODE = 'eventlet'
SOCKETIO_REDIS_URL = 'redis://localhost:6379/0'

CELERY_BROKER_URL = 'redis://localhost:6379/0'

VERSION = '0.0.1'

MPD_SERVER_CONF = {
    'host': 'localhost',
    'port': '6600'
}

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'mserver.db'))

SONG_SOURCES_CONFIG = {
    'youtube': {
        'api_key': os.getenv('YOUTUBE_API_KEY')
    }
}
