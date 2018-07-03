import { initApiEndpoints, getFullUlrs, initApiCaller } from './utils'

const endpoints = {
  rpc: {
    system_status: '/rpc/system-status'
  },
  srpc: {
    search_sources: '/srpc/player-sources',
    player_status: '/srpc/player-status'
  },
  search: '/search',
  auth: {
    login: '/auth',
    self: '/auth/self'
  }
}

export const urls = getFullUlrs(endpoints)

export const getEndpoints = token => {
  initApiCaller(token)
  return initApiEndpoints(endpoints)
}

export default endpoints
