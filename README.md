# Music Web Server

Web server that works as a shared frontend to Music Player Daemon.

The whole documentation is based on Debian based distributions.

## Introduction

Running the server requires redis and a celery workers.

## Dev Server

Web Server:
```
python mserver run_server
```

Listen to MPD events so that UI can by synced:

```
python mserver listen_mpd
```

And start celery worker

```
celery -A mserver.application.celery worker -l info
```