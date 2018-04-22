/* eslint-disable camelcase */
const handlers = {
  user_joined ({state, commit}, {message}) {
    commit('addNotification', {message})
  },
  user_left ({state, commit}, {message}) {
    commit('addNotification', {message})
  },
  player_play ({state, commit}, data) {
    commit('togglePlaying', true)
  },
  player_pause ({state, commit}, data) {
    commit('togglePlaying', false)
  },
  player_song_added ({state, commit}, {song, playlist}) {
    let message = `Nueva cancion en cola: ${song.title}`
    commit('addNotification', {message})
  },
  player_song_available ({state, commit}, song) {
    let message = `Nueva cancion disponible: ${song.title}`
    commit('addNotification', {message})
  },
  player_song_downloading ({state, commit}, song) {
    let message = `Descargando ${song.title}`
    commit('addNotification', {message})
  }
}

export default handlers
