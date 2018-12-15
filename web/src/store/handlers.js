/* eslint-disable camelcase */

function getMessageFromError(debug, { message, key, detail }) {
  let hrmessage = `Ha ocurrido un error ${message || key}`
  switch (key) {
    case 'player.song_add_error': {
      hrmessage = 'Error agregando canción'
      break
    }
    case 'player.song_download_error': {
      hrmessage = 'Error descargando canción'
      break
    }
  }

  let song = detail.song
  if (song) {
    hrmessage += ` ${song.ititle}`
  }

  if (debug) {
    hrmessage += `\n${message}`
  }

  return hrmessage
}

const handleError = ({ state, commit }, error) => {
  let message = getMessageFromError(state.server.debug, error)
  commit('addNotification', { message, error: true })
}

const handlers = {
  user_joined({ state, commit }, { message }) {
    // commit('addNotification', { message })
  },
  user_left({ state, commit }, { message }) {
    // commit('addNotification', { message })
  },
  player_play({ state, commit }, data) {},
  player_pause({ state, commit }, data) {},
  player_status({ state, dispatch }, data) {
    dispatch('setPlayerStatus', data)
  },
  player_previous({ dispatch }, song) {
    dispatch('startTimeUpdater')
  },
  player_next({ dispatch }, song) {
    dispatch('startTimeUpdater')
  },
  player_current({ dispatch, commit }, song) {
    commit('setCurrentSong', song)
    dispatch('setupSongTime')
  },
  player_song_added({ state, commit, dispatch }, song) {
    let message = `Nueva cancion en lista: ${song.title}`
    commit('addNotification', { message })
  },
  player_song_available({ state, commit }, song) {
    let message = `Nueva cancion disponible: ${song.title}`
    commit('addNotification', { message })
  },
  player_song_downloading({ state, commit }, song) {
    let message = `Descargando ${song.title}`
    commit('addNotification', { message })
  },
  player_song_removed({ state, commit }, song) {
    let message = `Canción eliminada: ${song.title}`
    commit('addNotification', { message })
  },
  player_playlist_changed({ dispatch }, data) {
    dispatch('refreshPlaylist')
  },
  disconnect({ commit, dispatch }, reason) {
    commit('onSocketConnectionStatusChange', reason)
    dispatch('setReconnectTimeout')
  },
  connect({ commit, dispatch }) {
    commit('onSocketConnectionStatusChange', null)
    dispatch('updatePlayerState')
  },
  error: handleError,
  player_song_add_error: handleError,
  player_song_download_error: handleError
}

export default handlers
