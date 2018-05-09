import handlers from './handlers'

/* eslint-disable camelcase */
const actions = {
  ...handlers,
  updateServerStatus ({state}, {success, data}) {
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
  initComm ({state, commit, dispatch}, {api, socket}) {
    commit('setComm', {api, socket})
    const events = [
      'player.play',
      'player.pause',
      'player.song_added',
      'player.song_available',
      'player.song_downloading',
      'user.joined',
      'user.left',
      'error'
    ]
    events.forEach(eventName => {
      let actionHandlerName = eventName.split('.').join('_')

      let method = (data) => {
        console.log(`${eventName}: ${JSON.stringify(data)}, ${actionHandlerName}`)
        commit('addEvent', data)
        dispatch(actionHandlerName, data)
      }
      socket.on(eventName, method)
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
    state.comm.socket.emit('player.download_song', song)
  },
  addSong ({state, commit}, song) {
    state.comm.socket.emit('player.add_song', song)
  }
}

export default actions
