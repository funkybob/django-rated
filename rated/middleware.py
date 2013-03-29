
from .settings import REALMS, DEFAULT_LIMIT, DEFAULT_TIMEOUT, REALM_MAP


class RatedMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Try to determine the realm for this view
        try:
            realm = request._rated_realm
        except AttributeError:
            try:
                realm = REALM_MAP[request.resolver_match.url_name]
            except KeyError:
                return None
        # should we also try the view name?

        conf = REALMS.get(realm, {})
        key = 'rated:%s:%s' % (realm, request.META['REMOTE_ADDR'],)
        now = time.time()
        # Do commands at once for speed
        pipe = redis.pipeline()
        # Add our timestamp to the range
        pipe.zadd(key, now, now)
        # Update to not expire for another hour
        pipe.expireat(key, now + conf.get('timeout', DEFAULT_TIMEOUT))
        # Remove old values
        pipe.zremrangebyscore(key, '-inf', now - HOUR)
        # Test count
        pipe.zcard(key)
        size = pipe.execute()[-1]
        if size > conf.get('limit', DEFAULT_LIMIT):
            return HttpResponse(status=501)
        return None
