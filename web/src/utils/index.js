const executeAlso = (fun, minorFun) => (params) => {
  minorFun()
  return fun(params)
}

const keepMaxLength = (array, maxLength) => {
  return array.splice(0, Math.min(array.length, maxLength))
}

export {
  executeAlso,
  keepMaxLength
}
