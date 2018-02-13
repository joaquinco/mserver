import axios from 'axios'

var RestApi;

function GetApiCaller(token) {
  return axios.create({
    baseURL: `http://localhost:5000/`,
    headers: {
      Authorization: 'Bearer {token}',
    }
  })
}

function InitApiCaller(token) {
  RestApi = GetApiCaller(token)
}

class Endpoint {
  constructor(endpoint) {
    this.endpoint = endpoint
  }

  async post(data) {
    var response = await RestApi.post(this.endpoint, data)
    return response
  }

  async get(params) {
    var response = await RestApi.get(this.endpoint, params)
    return response
  }
}
