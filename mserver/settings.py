import os

DEBUG = True

SECRET_KEY = b'\xd0H\xbdA\xdb`\xa5\x86\xca\x1d\xc2\xd6Z\x89\xa5\x8e\x0e\x0c\x93\xfaDCh\x91C)yh\xe5xxx'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MUSIC_DIR = os.path.join(BASE_DIR, 'storage')

if not os.path.exists(MUSIC_DIR):
    os.mkdir(MUSIC_DIR)
