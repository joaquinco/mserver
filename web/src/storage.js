const actualStorage = {
  set (key, value) {
    if (typeof value === 'object') {
      value = JSON.stringify(value)
    }
    localStorage.setItem(key, value)
  },
  get (key) {
    return localStorage.getItem(key)
  }
}

const dummyStorage = {
  set (key, value) {},
  get (key) {
    return null
  }
}

var storage

if (typeof Storage !== 'undefined') {
  storage = actualStorage
} else {
  storage = dummyStorage
}

export default storage
