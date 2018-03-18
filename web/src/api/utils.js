import axios from 'axios'
import io from 'socket.io-client'

const BASE_URL = 'http://192.168.1.197:5000'
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

  post (config) {
    return RestApi.post(this.endpoint, config)
  }

  get (config) {
    return RestApi.get(this.endpoint, config)
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
  return new Promise((resolve, reject) => {
    try {
      var socket = io(BASE_URL, {
        transportOptions: {
          polling: {
            extraHeaders: {
              'Authorization': 'Bearer ' + token
            }
          }
        }
      })
      resolve(socket)
    } catch (error) {
      reject(error)
    }
  })
}
