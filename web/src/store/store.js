import Vuex from 'vuex'

import actions from './actions'
import mutations from './mutations'
import getters from './getters'
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
      socket: null,
      error: null
    },
    auth: {
      access_token: null
    },
    playlist: {
      songs: [],
      current: {},
      currentTime: null,
      totalTime: null,
      _timer: null
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
    },
    views: {
      notification_tab_visible: false
    }
  },
  mutations,
  actions,
  getters
})

export default store
