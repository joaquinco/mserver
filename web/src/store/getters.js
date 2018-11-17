export default {
  isConnected({ comm: { socket } }) {
    return socket && socket.connected
  }
}
