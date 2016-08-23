import wrapt

from .settings import DEFAULT_REALM
from .utils import BACKEND


def rate_limit(realm=None):
    '''Apply rate limiting directly to any view-like function.'''
    if realm is None:
        realm = DEFAULT_REALM

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        request = args[0]
        source = BACKEND.source_for_request(request)
        if BACKEND.check_realm(source, realm):
            return BACKEND.make_limit_response(realm)
        return wrapped(*args, **kwargs)

    return wrapper
