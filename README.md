# Music web server

Flask web server with socketio server. Servs as a shared frontend to
Music Player Daemon.

The whole documentation is based on debian based distributions.

## Introduction

Running the server requires redis and a celery workers.

## Dev Server

```
flask run
```

And start celery worker

```
celery -A mserver.application.celery worker -l info
```