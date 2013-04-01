
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

        conf = settings.REALMS.get(realm, {})
        key = 'rated:%s:%s' % (realm, request.META['REMOTE_ADDR'],)
        now = time.time()

        client = redis.Redis(connection_pool=POOL)
        # Do commands at once for speed
        pipe = client.pipeline()
        # Add our timestamp to the range
        pipe.zadd(key, now, now)
        # Update to not expire for another hour
        pipe.expireat(key, now + conf.get('timeout', settings.DEFAULT_TIMEOUT))
        # Remove old values
        pipe.zremrangebyscore(key, '-inf', now - settings.DEFAULT_TIMEOUT)
        # Test count
        pipe.zcard(key)
        size = pipe.execute()[-1]
        if size > conf.get('limit', settings.DEFAULT_LIMIT):
            return HttpResponse(status=501)
        return None
