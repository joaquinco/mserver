const actualStorage = {
  set (key, value) {
    if (typeof value === 'object') {
      value = JSON.stringify(value)
    }
    localStorage.setItem(key, value)
  },
  get (key) {
    let ret = localStorage.getItem(key)
    try {
      return JSON.parse(ret)
    } catch (error) {
      return ret
    }
  }
}

const dummyStorage = {
  _store: {},
  set (key, value) {
    this._store[key] = value
  },
  get (key) {
    try {
      return this._store[key]
    } catch (error) {
      return null
    }
  }
}

var storage

if (typeof Storage !== 'undefined') {
  storage = actualStorage
} else {
  storage = dummyStorage
}

export default storage
