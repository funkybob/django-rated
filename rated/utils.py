
import time
import redis

from django.http import HttpResponse

from . import settings

# Connection pool
POOL = redis.ConnectionPool(**settings.REDIS)

class RateLimitBackend(object):

    def source_for_request(self, request):
        '''Return a source identifier for a request'''
        try:
            return request.META['X-Forwarded-For']
        except KeyError:
            pass
        return request.META['REMOTE_ADDR']

    def make_limit_response(self, realm):
        conf = settings.REALMS.get(realm, {})

        return HttpResponse(conf.get('message', settings.RESPONSE_MESSAGE),
            status=conf.get('code', settings.RESPONSE_CODE)
        )

    def check_realm(self, source, realm):
        '''
        Check if `source` has reached their limit in `realm`.

        Returns True if limit is reached.
        '''
        conf = settings.REALMS.get(realm, {})

        # Check against Realm whitelist
        if source in conf.get('whitelist', settings.DEFAULT_WHITELIST):
            return None

        key = 'rated:%s:%s' % (realm, source,)
        now = time.time()

        client = redis.Redis(connection_pool=POOL)
        # Do commands at once for speed
        # We don't need these to operate in a transaction, as none of the values
        # we send are dependant on values in the DB
        pipe = client.pipeline(transaction=False)
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

BACKEND = RateLimitBackend()

