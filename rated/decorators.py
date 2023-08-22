import time
from functools import partial

import redis
from django.conf import settings
from django.http import HttpResponse

from .signals import rate_limited

# Connection pool
POOL = redis.ConnectionPool(**getattr(settings, 'RATED_REDIS', {}))


class RateLimit:
    def __init__(self, func, realm=None):
        self.func = func
        if realm is None:
            realm = 'default'
        self.realm = realm

    def __call__(self, request, *args, **kwargs):
        source = self.get_request_source(request)

        if self.check_realm(source):
            rate_limited.send_robust(self.realm, client=source)
            return self.make_limit_response()

        return self.func(request, *args, **kwargs)

    @property
    def conf(self):
        return getattr(settings, 'RATED_REALMS', {}).get(self.realm, {})

    def get_request_source(self, request):
        '''Return a source identifier for a request'''
        if getattr(settings, 'USE_X_FORWARDED_FOR', False):
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                return x_forwarded_for.split(',')[0]

        return request.META.get('REMOTE_ADDR')

    def check_realm(self, source):
        '''
        Check if `source` has reached their limit in `realm`.

        Returns True if limit is reached.
        '''
        # Check against Realm allowed list
        allowed = self.conf.get('allowed', getattr(settings, 'RATED_DEFAULT_ALLOWED', []))
        if source in allowed:
            return None

        key = f'rated:{self.realm}:{source}'
        now = time.time()

        duration = self.conf.get('duration', getattr(settings, 'RATED_DEFAULT_DURATION', 60 * 60))
        limit = self.conf.get('limit', getattr(settings, 'RATED_DEFAULT_LIMIT', 100))

        client = redis.Redis(connection_pool=POOL)
        # Do commands at once for speed
        # We don't need these to operate in a transaction, as none of the
        # values we send are dependant on values in the DB
        with client.pipeline(transaction=False) as pipe:
            # Add our timestamp to the range
            pipe.zadd(key, { str(now):  now })
            # Update to not expire for another DURATION
            pipe.expireat(key, int(now + duration))
            # Remove old values
            pipe.zremrangebyscore(key, '-inf', now - duration)
            # Test count
            pipe.zcard(key)
            size = pipe.execute()[-1]
        return size > limit

    def make_limit_response(self):
        return HttpResponse(
            self.conf.get(
                'message',
                getattr(settings, 'RATED_RESPONSE_MESSAGE', 'Too many requests'),
            ),
            status=self.conf.get('code', getattr(settings, 'RATED_RESPONSE_CODE', 429)),
        )


def rate_limit(func=None, **kwargs):
    """
    When you use `@rate_limit` then func is set.
    When you use `@rate_limit()` then func is None.
    When you use `@rate_limit(key=val)` then func is None.

    Only in the first case do we need to invoke the decorator;
    Python will do it otherwise.
    """
    if func is None:
        return partial(RateLimit, **kwargs)
    return RateLimit(func, **kwargs)
