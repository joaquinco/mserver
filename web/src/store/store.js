import Vuex from 'vuex'

import actions from './actions'
import mutations from './mutations'
import Vue from 'vue'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    server: {
      checked: false,
      available: false,
      version: ''
    },
    comm: {
      api: null,
      socket: null
    },
    auth: {
      token: null,
      user: null
    },
    playlist: {
      songs: [],
      fetching: false
    },
    search: {
      sources: [],
      results: {}
    },
    player: {
      playing: false
    }
  },
  mutations,
  actions
})

export default store
