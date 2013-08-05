
from django.conf import settings

DEFAULT_REALM = getattr(settings, 'RATED_DEFAULT_REALM', 'default')
DEFAULT_LIMIT = getattr(settings, 'RATED_DEFAULT_LIMIT', 100)
DEFAULT_TIMEOUT = getattr(settings, 'RATED_DEFAULT_TIMEOUT', 60 * 60)

RESPONSE_CODE = getattr(settings, 'RATED_RESPONSE_CODE', 429)
RESPONSE_MESSAGE = getattr(settings, 'RATED_RESPONSE_MESSAGE', '')

DEFAULT_WHITELIST = getattr(settings, 'RATED_DEFAULT_WHITELIST', [])

REALMS = getattr(settings, 'RATED_REALMS', {})

REALM_MAP = getattr(settings, 'RATED_REALM_MAP', {})

# Redis config parameters
REDIS = getattr(settings, 'RATED_REDIS', {})

