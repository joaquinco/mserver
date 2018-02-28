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
  setUser ({state}, {username, is_superuser}) {
    state.user = {...state.user, username, is_superuser}
  }
}

export default actions
