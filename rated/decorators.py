
from functools import partial, wraps

from .middleware import RatedMiddleware
from .settings import DEFAULT_REALM

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
        result = RatedMiddleware().process_view(request, func, args, kwargs)
        if result is None:
            return func(request, *args, **kwargs)
        return result

    rated_realm(_inner, realm)

    return _inner

def rate_limit_method(func=None, realm=None):
    '''Rate limit a view-like method'''
    if func is None:
        return partial(rate_limit_method, realm=realm)

    @wraps(func)
    def _inner(self, request, *args, **kwargs):
        result = RatedMiddleware().process_view(request, func, args, kwargs)
        if result is None:
            return func(self, request, *args, **kwargs)
        return result

    rated_realm(func, realm)

    return _inner
