import Vuex from 'vuex'

import actions from './actions'
import mutations from './mutations'

const store = new Vuex.Store({
  state: {
    status: {
      server: {
        checked: false,
        available: false,
        version: ''
      },
      socket: {
        conected: false,
        socket: null
      }
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
  mutations: {
    ...mutations
  },
  actions: {
    ...actions
  }
})

export default store
