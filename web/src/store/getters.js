export default {
  isConnected({ comm: { socket } }) {
    return socket && socket.connected
  },
  searchSourcesByName({ search: { sources } }) {
    let ret = {}

    sources.forEach(source => {
      ret[source.name] = source
    })

    return ret
  }
}
