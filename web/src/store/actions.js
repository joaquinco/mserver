/* eslint-disable camelcase */
const actions = {
  updateServerStatus ({state}, {success, data}) {
    if (success) {
      state.server = {...state.server,
        checked: true,
        available: true,
        version: data.version
      }
    } else {
      state.server.checked = true
    }
  },
  initComm ({state, commit}, {api, socket}) {
    commit('setComm', {api, socket})
    const events = [
      'player.play',
      'player.pause',
      'player.song_added',
      'player.song_available',
      'player.song_downloading',
      'user.joined',
      'user.left'
    ]
    events.forEach(eventName => {
      socket.on(eventName, data => console.log(eventName, JSON.stringify(data)))
    })
  },
  setUser ({state}, {username, is_superuser}) {
    state.user = {...state.user, username, is_superuser}
  },
  clearSearchResults ({state, commit}) {
    state.search.sources.forEach(source => {
      commit('setSearchResults', {source: source.name, results: []})
    })
  },
  setSearchSources ({state, commit}, sources) {
    state.search.sources = sources
    commit('setSearchSources', sources)
    sources.forEach(source => {
      commit('setSearchResults', {source: source.name, results: []})
    })
  },
  downloadSong ({state, commit}, song) {
    state.comm.socket.emit('player.add_song', song)
  },
  addSong ({state, commit}, song) {
    state.comm.socket.emit('player.download_song', song)
  }
}

export default actions
