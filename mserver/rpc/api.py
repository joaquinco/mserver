_rpcs = {}

_secure_rpcs = {}


def _get_rpcs(secure=False):
    global _secure_rpcs
    global _rpcs

    if secure:
        return _secure_rpcs
    else:
        return _rpcs


def handle_rpc_error(rpc_fn):
    def rpc_wrapper(*args, **kwargs):
        try:
            return rpc_fn(*args, **kwargs)
        except Exception as e:
            # TODO: Handle this exception
            raise e

    return rpc_wrapper


def register(rpc_name, rpc_fn, secure=False):
    """
    Secure rpc need user authentication.
    """
    global _rpcs
    _get_rpcs(secure)[rpc_name] = handle_rpc_error(rpc_fn)


def call(rpc_name, *args, secure=False, **kwargs):
    try:
        return _get_rpcs(secure)[rpc_name](*args, **kwargs)
    except KeyError:
        # TODO: Handle or re-raise this exception
        raise
