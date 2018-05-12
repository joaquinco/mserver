# General documentation

## A&A

To use every API endpoint and sockets an access token is required.
The token is obtained calling the authentication endpoint and sent
in the Authorization header with Bearer realm.

## Flask Socket IO

To enable CORS preflights packets on socketio connect endpoint a monkey
patch had to be made. Since this request is handled separately from
standard flask request the flask-cors module didn't recognise it.

The patch consisted in calling the default request handler when calling
the socket io endpoint with OPTIONS method. Then a dummy view was added
with the exact same path as the socketio endpoint so that flask-cors
will create the preflight packages properly and uniformly.

## SocketIO

Uses Redis as message_queue, to enable worker process to emit socketio
events from different processes.