import os
import datetime

DEBUG = True

SECRET_KEY = b'\xd0H\xbdA\xdb`\xa5\x86\xca\x1d\xc2\xd6Z\x89\xa5\x8e\x0e\x0c\x93\xfaDCh\x91C)yh\xe5xxx'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MUSIC_DIR = os.path.join(BASE_DIR, 'storage')

if not os.path.exists(MUSIC_DIR):
    os.mkdir(MUSIC_DIR)

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