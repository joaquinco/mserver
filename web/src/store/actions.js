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
  setComm ({state}, {api, socket}) {
    state.comm = {
      api, socket
    }
  }
}

export default actions
