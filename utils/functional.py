def compose(*funs):
    """
    Return a function where the result of its evaluation is the result of the composition from
    left to right of the functions passed as arguments. Argument incompatibility is not checked.
    """

    def composed_funs(*args, **kwargs):
        ret = funs[0](*args, **kwargs)
        for fun in funs[1:]:
            ret = fun(ret)
        return ret

    return composed_funs
