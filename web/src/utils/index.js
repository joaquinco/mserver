const executeAlso = (fun, minorFun) => (params) => {
  minorFun()
  return fun(params)
}

export { executeAlso }
