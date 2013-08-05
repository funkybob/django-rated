
from . import settings

from django.http import HttpResponse

import time
import redis

# Connection pool
POOL = redis.ConnectionPool(**settings.REDIS)

class RatedMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Try to determine the realm for this view
        try:
            realm = view_func._rated_realm
        except AttributeError:
            try:
                realm = settings.REALM_MAP[request.resolver_match.url_name]
            except KeyError:
                return None
        # should we also try the view name?

        source = request.META['REMOTE_ADDR']

        conf = settings.REALMS.get(realm, {})

        # Check against Realm whitelist
        if source in conf.get('whitelist', settings.DEFAULT_WHITELIST):
            return None

        key = 'rated:%s:%s' % (realm, source,)
        now = time.time()

        client = redis.Redis(connection_pool=POOL)
        # Do commands at once for speed
        pipe = client.pipeline()
        # Add our timestamp to the range
        pipe.zadd(key, now, now)
        # Update to not expire for another hour
        pipe.expireat(key, int(now + conf.get('timeout', settings.DEFAULT_TIMEOUT)))
        # Remove old values
        pipe.zremrangebyscore(key, '-inf', now - settings.DEFAULT_TIMEOUT)
        # Test count
        pipe.zcard(key)
        size = pipe.execute()[-1]
        if size > conf.get('limit', settings.DEFAULT_LIMIT):
            return HttpResponse(conf.get('message', settings.RESPONSE_MESSAGE),
                status=conf.get('code', settings.RESPONSE_CODE, 429)
            )
        return None
