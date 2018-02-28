/* eslint-disable camelcase */
const mutations = {
  setComm (state, {api, socket}) {
    state.comm = {
      api, socket
    }
  },
  setToken (state, access_token) {
    state.auth.access_token = access_token
  },
  setSearchSources (state, sources) {
    state.search.sources = sources
  }
}

export default mutations
