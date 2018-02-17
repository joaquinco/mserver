const mutations = {
  setComm (state, {api, socket}) {
    state.comm = {
      api, socket
    }
  }
}

export default mutations
