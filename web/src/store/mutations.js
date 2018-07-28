import { keepMaxLength } from '@/utils'

const maxEventsStored = 100
const maxNotificationsStored = 20

/* eslint-disable camelcase */
const mutations = {
  setComm(state, { api, socket }) {
    state.comm = {
      api,
      socket
    }
  },
  setToken(state, access_token) {
    state.auth.access_token = access_token
  },
  setSearchSources(state, sources) {
    state.search.sources = sources
  },
  setSearchResults(state, { source, results }) {
    state.search.results = { ...state.search.results, [source]: results }
  },
  addEvent(state, data) {
    let events = state.async.events.slice()
    events.push(data)
    state.async = {
      ...state.async,
      events: keepMaxLength(events, maxEventsStored)
    }
  },
  addNotification(state, { message, error }) {
    let now = new Date()

    let notification = {
      message,
      created: now,
      showed: false,
      error: !!error,
      id: now.toISOString()
    }

    let notifications = state.async.notifications.slice()
    notifications.unshift(notification)
    state.async = {
      ...state.async,
      notifications: keepMaxLength(notifications, maxNotificationsStored)
    }
  },
  clearNotifications(state) {
    state.async = { ...state.async, notifications: [] }
  },
  setPlayerStatus(state, status) {
    state.player = { ...state.player, ...status }
  },
  setCurrentPlaylistSongs(state, songs) {
    state.playlist = { ...state.playlist, songs }
  },
  setCurrentSong(state, song) {
    state.playlist = { ...state.playlist, current: song }
  },
  toggleNotificationTab(state) {
    let notification_tab_visible = !state.views.notification_tab_visible
    state.views = { ...state.views, notification_tab_visible }
  }
}

export default mutations
