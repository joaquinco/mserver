const actions = {
  updateServerStatus: function ({ state }, success, data) {
    if (success) {
      state.server = {
        checked: true,
        available: true,
        version: data.version
      }
    } else {
      state.server.checked = true
    }
  }
}

export default actions
