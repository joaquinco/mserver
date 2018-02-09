# Mserver API documentation

## HTTP Endpoints

- `/api/search`:

GET
```yaml
- name: query
  type: query
  required: true
  description: what to search
- name: source
  type: query
  required: false
  description: where to search
```

- `/api/auth`

POST
```yaml
- name: username
  type: body
  required: true
- name: password
  type: body
  required: true
```

- `/api/rpc/<rpc_name>`

Calls a method and returns its result.

GET, POST
```yaml
- name: rpc_name
  type: string
  location: path
  description: name of RP
```

POST
```yaml
- name: args
  type: list
  location: body
  description: positional arguments
  required: false
- name: kwargs
  type: dict
  description: key word arguments
  required: false
```

Two types of arguments can be sent:
- args: positional arguments, available only from POST
- kwargs: key word arguments. Can be sent through the POST body and the
search arguments.

## SocketIO Events

- `user.joined`: receive
- `user.left`: receive
- `player.play`: send, receive
- `player.pause`: send, receive
- `player.add_son`: send
- `player.song_added`: receive
- `player.song_available`: receive