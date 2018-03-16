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
  },
  setSearchResults (state, {source, results}) {
    state.search.results = {...state.search.results, [source]: results}
  }
}

export default mutations
