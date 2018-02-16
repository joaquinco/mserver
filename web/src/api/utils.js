import axios from 'axios'
import io from 'socket.io-client'

const BASE_URL = 'http://localhost:5000'
const BASE_API_URL = `${BASE_URL}/api`

var RestApi = null

function getApiCaller (token) {
  return axios.create({
    baseURL: BASE_API_URL,
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
}

export function initApiCaller (token) {
  RestApi = getApiCaller(token)
}

class Endpoint {
  constructor (endpoint) {
    this.endpoint = endpoint
  }

  async post (data) {
    var response = await RestApi.post(this.endpoint, data)
    return response
  }

  async get (params) {
    var response = await RestApi.get(this.endpoint, params)
    return response
  }
}

function recursiveMap (obj, result, fun) {
  Object.entries(obj).forEach(([key, value]) => {
    if (typeof value !== 'object') {
      result[key] = fun(value)
    } else {
      var deeperResult = {}
      recursiveMap(value, deeperResult, fun)
      result[key] = deeperResult
    }
  })
}

function callRecursiveMap (obj, fun) {
  var ret = {}

  recursiveMap(obj, ret, fun)

  return ret
}

export const initApiEndpoints = (endpoints) => callRecursiveMap(endpoints, value => new Endpoint(value))
export const getFullUlrs = (endpoints) => callRecursiveMap(endpoints, value => BASE_API_URL + value)

export function getSocket (token) {
  var socket = io(BASE_URL, {
    transportOptions: {
      polling: {
        extraHeaders: {
          'Authorization': 'Bearer ' + token
        }
      }
    }
  })
  return socket
}
