_rpcs = {}


def handle_rpc_error(rpc_fn):
    def rpc_wrapper(*args, **kwargs):
        try:
            return rpc_fn(*args, **kwargs)
        except Exception as e:
            # TODO: Handle this exception
            raise e

    return rpc_wrapper


def register(rpc_name, rpc_fn):
    global _rpcs
    _rpcs[rpc_name] = handle_rpc_error(rpc_fn)


def call(rpc_name, *args, **kwargs):
    global _rpcs
    try:
        return _rpcs[rpc_name](*args, **kwargs)
    except KeyError:
        # TODO: Handle or re-raise this exception
        raise
