import { keepMaxLength } from '@/utils'

const maxEventsStored = 100
const maxNotificationsStored = 20

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
  },
  addEvent (state, data) {
    let events = state.async.events.slice()
    events.push(data)
    state.async = {...state.async, events: keepMaxLength(events, maxEventsStored)}
  },
  addNotification (state, {message}) {
    let now = new Date()

    let notification = {
      message,
      created: now,
      showed: false,
      id: now.toISOString()
    }

    let notifications = state.async.notifications.slice()
    notifications.push(notification)
    state.async = {...state.async, notifications: keepMaxLength(notifications, maxNotificationsStored)}
  },
  togglePlaying (state, playing) {
    state.player = {...state.player, playing}
  }
}

export default mutations
