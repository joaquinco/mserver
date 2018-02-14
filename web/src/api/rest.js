import { initApiEndpoints, getFullUlrs, initApiCaller } from './utils'

const endpoints = {
  rpc: {
    system_status: '/rpc/system-status'
  },
  search: '/search',
  auth: '/auth'
}

export const urls = getFullUlrs(endpoints)

export const getEndpoints = (token) => {
  initApiCaller(token)
  return initApiEndpoints(endpoints)
}

export default endpoints
