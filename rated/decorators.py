
from functools import wraps, partial

from .settings import DEFAULT_REALM

def rated_realm(func=None, realm=None):
    '''Annotate a view for a given realm.'''
    if func is None:
        return partial(rated_realm, realm=realm)
    func._rated_realm = realm or settings.DEFAULT_REALM
    return func

