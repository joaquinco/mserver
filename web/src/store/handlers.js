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

const handlers = {
  user_joined({ state, commit }, { message }) {
    commit('addNotification', { message })
  },
  user_left({ state, commit }, { message }) {
    commit('addNotification', { message })
  },
  player_play({ state, commit }, data) {},
  player_pause({ state, commit }, data) {},
  player_status({ state, commit }, data) {
    commit('setPlayerStatus', data)
  },
  player_previous({ commit }, song) {},
  player_next({ state, commit }, song) {},
  player_current({ state, commit }, song) {
    commit('setCurrentSong', song)
  },
  player_song_added({ state, commit, dispatch }, song) {
    let message = `Nueva cancion en cola: ${song.title}`
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
  error({ state, commit }, error) {
    let message = getMessageFromError(state.server.debug, error)
    commit('addNotification', { message, error: true })
  },
  disconnect({ state, commit }, reason) {
    commit('onSocketDisconnected', reason)
  }
}

export default handlers
