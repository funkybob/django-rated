
from . import settings
from .decorators import rate_limit
from .signals import rate_limited


class RatedMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Try to determine the realm for this view
        try:
            realm = settings.REALM_MAP[request.resolver_match.url_name]
        except KeyError:
            pass  # Fall through to return
        else:
            limiter = rate_limit(None, realm=realm)
            source = limiter.get_request_source(request)

            if limiter.check_realm(source):
                rate_limited.send_robust(realm, client=source)
                return limiter.make_limit_response()

        return self.get_response(request)
