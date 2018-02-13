import { initApiEndpoints, getFullUlrs } from './utils'

const endpoints = {
  rpc: {
    system_status: '/rpc/system-status'
  },
  search: '/search',
  auth: '/auth'
}

export const urls = getFullUlrs(endpoints)

export const getEndpoints = () => initApiEndpoints(endpoints)

export default endpoints
