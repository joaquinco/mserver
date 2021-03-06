import handlers from './handlers'
import config from '@/config'

const socketioEvents = [
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
  'disconnect',
  // Errors
  'error',
  'player.song_add_error',
  'player.song_download_error'
]

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
    var debug = state.server.debug
    socketioEvents.forEach(eventName => {
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
    // Since events are attached after connection we have to manually set this:
    dispatch('updatePlayerState')
  },
  setUser({ state }, { username, is_superuser }) {
    state.user = { ...state.user, username, is_superuser }
  },
  clearSearchResults({ state, commit }) {
    state.search.sources.forEach(source => {
      commit('setSearchResults', { source: source.name, results: [] })
    })
  },
  setSearchSources({ commit }, sources) {
    let sortedSources = sources.sort((a, b) => a.ordering - b.ordering)
    commit('setSearchSources', sortedSources)
    sources.forEach(({ name }) => {
      commit('setSearchResults', { source: name, results: [] })
    })
  },
  removeSongFromSearchList({ state, commit }, song) {
    let searchedSongs = state.search.results[song.source]
    let remainingSongs = searchedSongs.filter(
      obj => obj.search_id !== song.search_id
    )
    commit('setSearchResults', { source: song.source, results: remainingSongs })
  },
  setSongAsAdded({ state, commit }, { source, search_id }) {
    const searchedSongs = state.search.results[source]
    const newSearchList = searchedSongs.map(song => {
      if (song.search_id === search_id) {
        return { ...song, isAlreadySelected: true }
      }
      return song
    })
    commit('setSearchResults', { source: source, results: newSearchList })
  },
  downloadSong({ state }, song) {
    state.comm.socket.emit('player.download_song', song)
  },
  addSong({ state, dispatch }, song) {
    state.comm.socket.emit('player.add_song', song)
    dispatch('setSongAsAdded', song)
  },
  removeSong({ state }, song) {
    state.comm.socket.emit('player.remove', song)
  },
  playNextSong({ state, dispatch }, song) {
    state.comm.socket.emit('player.add_song_next', song)
    dispatch('setSongAsAdded', song)
  },
  playSong({ state }, song) {
    state.comm.socket.emit('player.playid', song)
  },
  onSongAction({ dispatch }, { action, song }) {
    console.log(action, song)
    dispatch(`${action}Song`, song)
  },
  refreshPlaylist({ state, commit }) {
    state.comm.api.playlist.get().then(response => {
      commit('setCurrentPlaylistSongs', response.data)
    })
  },
  updateDB({ state }) {
    state.comm.socket.emit('player.updatedb')
  },
  toggleMPDConfiguration({ state }, configuration_name) {
    state.comm.socket.emit(`player.${configuration_name}`, {
      value: !state.player.status[configuration_name]
    })
  },
  clearPlaylist({ state }) {
    state.comm.socket.emit('player.clear')
  },
  setCrossfade({ state }, value) {
    state.comm.socket.emit('player.crossfade', { value })
  },
  incrementSongTime({ state, commit, dispatch }) {
    let { currentTime, totalTime } = state.playlist

    if (currentTime != null && totalTime != null) {
      currentTime += 1

      if (totalTime - currentTime < 0) {
        dispatch('stopTimeUpdater')
      } else {
        commit('setCurrentSongTime', { currentTime })
      }
    }
  },
  setupSongTime({ state, commit }) {
    const { time } = state.player.status

    if (time) {
      const parts = time.split(':')
      let currentTime, totalTime

      try {
        currentTime = parseInt(parts[0])
        totalTime = parseInt(parts[1])
      } catch (err) {
        commit('setCurrentSongTime', { currentTime: null, totalTime: null })
      }
      commit('setCurrentSongTime', { currentTime, totalTime })
    }
  },
  startTimeUpdater({ state, commit, dispatch }) {
    dispatch('stopTimeUpdater')
    dispatch('setupSongTime')
    let { totalTime } = state.playlist

    if (totalTime) {
      const _timer = setInterval(() => dispatch('incrementSongTime'), 1000)
      commit('setCurrentSongTime', { _timer })
    }
  },
  stopTimeUpdater({ state, commit }) {
    let { _timer } = state.playlist
    clearInterval(_timer)
    commit('setCurrentSongTime', { _timer: null })
  },
  updatePlayerState({ state, dispatch }) {
    const { api, socket } = state.comm

    api.srpc.player_status.get().then(
      ({ data }) => {
        dispatch('setPlayerStatus', data)
        socket.emit('player.current')
      },
      error => {
        this.error = error
      }
    )
  },
  setPlayerStatus({ commit, dispatch }, data) {
    commit('setPlayerStatus', data)
    if (data.status.state === 'play') {
      dispatch('startTimeUpdater')
    } else {
      dispatch('stopTimeUpdater')
    }
  },
  setReconnectTimeout({ dispatch }) {
    setTimeout(
      () => dispatch('checkReconnect'),
      config.reconnect_check_interval
    )
  },
  checkReconnect({ state, dispatch }) {
    const { socket } = state.comm
    if (!socket.connected) {
      socket.connect()
      dispatch('setReconnectTimeout')
    }
  }
}

export default actions
