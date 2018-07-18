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
      version: '',
      debug: false
    },
    user: {
      username: '',
      is_superuser: false
    },
    comm: {
      api: null,
      socket: null
    },
    auth: {
      access_token: null
    },
    playlist: {
      songs: [],
      current: {}
    },
    search: {
      sources: [],
      results: {}
    },
    player: {
      stats: {},
      status: {},
      version: null
    },
    async: {
      notifications: [],
      events: []
    }
  },
  mutations,
  actions
})

export default store
