
from functools import partial, wraps

from .settings import DEFAULT_REALM
from .utils import BACKEND

def rated_realm(func=None, realm=None):
    '''Annotate a view for a given realm.'''
    if func is None:
        return partial(rated_realm, realm=realm)
    func._rated_realm = realm or DEFAULT_REALM
    return func

def rate_limit(func=None, realm=None):
    '''Apply rate limiting directly to any view-like function.'''
    if func is None:
        return partial(rate_limit, realm=realm)

    @wraps(func)
    def _inner(request, *args, **kwargs):
        source = BACKEND.source_for_request(request)
        if BACKEND.check_realm(source, realm):
            return BACKEND.make_limit_response(realm)
        return func(request, *args, **kwargs)

    return _inner

def rate_limit_method(func=None, realm=None):
    '''Rate limit a view-like method'''
    if func is None:
        return partial(rate_limit_method, realm=realm)

    @wraps(func)
    def _inner(self, request, *args, **kwargs):
        source = BACKEND.source_for_request(request)
        if BACKEND.check_realm(source, realm):
            return BACKEND.make_limit_response(realm)
        return func(self, request, *args, **kwargs)

    return _inner
