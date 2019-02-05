# Music Web Server

Web server that works as a shared web frontend to Music Player Daemon.

Tested on Debian based Linux.

## Notes

The objective of this project was just to learn.

Front end language: ES

## Dependencies

- Redis
- Python3

## Configure

> TODO

## Running Server and Services

> Release version is not ready.

Web Server:
```
./bin/mserver run_server [-h bind_address] [-p bind_port]
```

Listen to MPD events so that UI can by synced:

```
./bin/mserver listen_mpd
```

And start celery workers

```
celery -A mserver.application.celery worker -l info
```

## On development

### Backend

The abave commands will execute the mserver module from the standard PYTHONPATH.
To execute the development project you must export `PYTHONPATH=/path/to/project` and run as above.

### Frontend

Under the web folder is the vuejs front end project. You can run it in development mode with:
```
npm run dev
```

Or compile it and serve it from backend with:
```
npm run build
```
