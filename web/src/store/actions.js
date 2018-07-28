import handlers from './handlers'

/* eslint-disable camelcase */
const actions = {
  ...handlers,
  updateServerStatus({ state }, { success, data }) {
    if (success) {
      state.server = {
        ...state.server,
        ...data,
        checked: true,
        available: true
      }
    } else {
      state.server = {
        ...state.server,
        checked: true,
        available: false
      }
    }
  },
  initComm({ state, commit, dispatch }, { api, socket }) {
    commit('setComm', { api, socket })
    const events = [
      'player.status',
      'player.play',
      'player.pause',
      'player.next',
      'player.previous',
      'player.current',
      'player.song_added',
      'player.song_available',
      'player.song_downloading',
      'player.playlist_changed',
      'user.joined',
      'user.left',
      'error',
      'disconnect'
    ]
    var debug = state.server.debug
    events.forEach(eventName => {
      let actionHandlerName = eventName.split('.').join('_')

      let method = data => {
        if (debug) {
          console.log(
            `${eventName}: ${JSON.stringify(data)}, ${actionHandlerName}`
          )
        }
        commit('addEvent', data)
        dispatch(actionHandlerName, data)
      }
      socket.on(eventName, method)
    })
  },
  setUser({ state }, { username, is_superuser }) {
    state.user = { ...state.user, username, is_superuser }
  },
  clearSearchResults({ state, commit }) {
    state.search.sources.forEach(source => {
      commit('setSearchResults', { source: source.name, results: [] })
    })
  },
  setSearchSources({ state, commit }, sources) {
    state.search.sources = sources
    commit('setSearchSources', sources)
    sources.forEach(source => {
      commit('setSearchResults', { source: source.name, results: [] })
    })
  },
  removeSongFromSearchList({ state, commit }, song) {
    let searchedSongs = state.search.results[song.source]
    let remainingSongs = searchedSongs.filter(
      obj => obj.search_id !== song.search_id
    )
    commit('setSearchResults', { source: song.source, results: remainingSongs })
  },
  downloadSong({ state }, song) {
    state.comm.socket.emit('player.download_song', song)
  },
  addSong({ state, dispatch }, song) {
    state.comm.socket.emit('player.add_song', song)
    dispatch('removeSongFromSearchList', song)
  },
  refreshPlaylist({ state, commit }) {
    state.comm.api.playlist.get().then(response => {
      commit('setCurrentPlaylistSongs', response.data)
    })
  }
}

export default actions
