
from . import settings
from .signals import rate_limited
from .utils import BACKEND


class RatedMiddleware(object):
    '''
    Middleware to check for annotated views on each request.
    '''

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Try to determine the realm for this view
        try:
            realm = settings.REALM_MAP[request.resolver_match.url_name]
        except KeyError:
            return None

        source = BACKEND.source_for_request(request)

        if BACKEND.check_realm(source, realm):
            rate_limited.send_robust(realm, client=source)
            return BACKEND.make_limit_response()

        return None
