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
  player_play({ state, commit }, data) {
    commit('togglePlaying', data)
  },
  player_pause({ state, commit }, data) {
    commit('togglePlaying', data)
  },
  player_song_added({ state, commit }, { song, playlist }) {
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
  error({ state, commit }, error) {
    let message = getMessageFromError(state.server.debug, error)
    commit('addNotification', { message, error: true })
  }
}

export default handlers
