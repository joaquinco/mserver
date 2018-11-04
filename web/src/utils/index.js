const executeAlso = (fun, minorFun) => (params) => {
  minorFun()
  return fun(params)
}

const keepMaxLength = (array, maxLength) => {
  return array.splice(0, Math.min(array.length, maxLength))
}

const zeroPad = (number) => (
  number < 10 ? `0${number}` : number.toString()
)

const formatTime = (seconds) => {
  let min = Math.round(seconds / 60)
  let sec = Math.round(seconds % 60)

  return `${zeroPad(min)}:${zeroPad(sec)}`
}

export {
  executeAlso,
  keepMaxLength,
  formatTime
}
