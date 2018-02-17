import storage from '@/storage'

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
  setUser ({state}, {username, is_superuser, access_token}) {
    state.auth.access_token = access_token
    state.user = {...state.user, username, is_superuser}
    storage.set('token', access_token)
  }
}

export default actions
