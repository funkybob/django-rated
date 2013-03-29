
from django.conf import settings

DEFAULT_REALM = getattr(settings, 'RATED_DEFAULT_REALM', 'default')
DEFAILT_LIMIT = getattr(settings, 'RATED_DEFAULT_LIMIT', 100)
DEFAULT_TIMEOUT = getattr(settings, 'RATED_DEFAULT_TIMEOUT', 60 * 60)

REALMS = getattr(settings, 'RATED_REALMS', {})

REALM_MAP = getattr(settings, 'RATED_REALM_MAP', {})

