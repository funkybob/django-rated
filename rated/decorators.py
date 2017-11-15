import time
from functools import partial

from django.http import HttpResponse
import redis

from . import settings
from .signals import rate_limited

# Connection pool
POOL = redis.ConnectionPool(**settings.REDIS)


class rate_limit:
    def __new__(cls, *args, **kwargs):
        if not args:
            return partial(cls, **kwargs)
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, func, realm=None):
        self.func = func
        if realm is None:
            realm = settings.DEFAULT_REALM
        self.realm = realm

    def __call__(self, request, *args, **kwargs):
        source = self.get_request_source(request)

        if self.check_realm(source):
            rate_limited.send_robust(self.realm, client=source)
            return self.make_limit_response()

        return self.func(request, *args, **kwargs)

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
        conf = settings.REALMS.get(self.realm, {})

        # Check against Realm whitelist
        if source in conf.get('whitelist', settings.DEFAULT_WHITELIST):
            return None

        key = 'rated:%s:%s' % (self.realm, source,)
        now = time.time()

        client = redis.Redis(connection_pool=POOL)
        # Do commands at once for speed
        # We don't need these to operate in a transaction, as none of the
        # values we send are dependant on values in the DB
        with client.pipeline(transaction=False) as pipe:
            # Add our timestamp to the range
            pipe.zadd(key, now, now)
            # Update to not expire for another DURATION
            pipe.expireat(key, int(now + conf.get('duration', settings.DEFAULT_DURATION)))
            # Remove old values
            pipe.zremrangebyscore(key, '-inf', now - settings.DEFAULT_DURATION)
            # Test count
            pipe.zcard(key)
            size = pipe.execute()[-1]
        return size > conf.get('limit', settings.DEFAULT_LIMIT)

    def make_limit_response(self):
        conf = settings.REALMS.get(self.realm, {})

        return HttpResponse(conf.get('message', settings.RESPONSE_MESSAGE),
                            status=conf.get('code', settings.RESPONSE_CODE))
