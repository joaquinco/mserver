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

## SocketIO Events

- `user.joined`: receive
- `user.left`: receive
- `player.play`: send, receive
- `player.pause`: send, receive
- `player.add_son`: send
- `player.song_added`: receive
- `player.song_available`: receive