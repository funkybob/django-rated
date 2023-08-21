=========
Changelog
=========

v2.0.0:
=======

+ Renamed "whitelist" to "allowed"
+ Droped middleware

v1.1.2:
=======

SECURITY RELEASE

+ X-Forwarded-For is no longer used by default.

You can enable the old behavior by setting USE_X_FORWARDED_FOR = True in your
settings.

v1.1.1:
=======

Bug fixes:

+ Corrected retrieval of IP from X-Forwarded-For header (thanks Nam!)
+ Pass 'realm' to make_limit_response in middleware (thanks Nam and Jesse!)

v1.1.0:
=======

Backward Incompatible Changes:

* rated_realm decorator is no longer supported
* TIMEOUT has been renamed to DURATION

Features:

+ Refactored code to share functions
+ Now supports X-Forwarded-For
+ Middleware is no longer required

v1.0.3:
=======

Features:

+ Add `rate_limited` signal
+ Add `rate_limit` decorator

v1.0.2:
=======

Bug fixes:

- Fix leftover code

v1.0.1:
=======

Bug fixes:

- Don't wrap pipeline call in transaction

v1.0.0:
=======

Features;

+ Added RATED_RESPONSE_CODE and RATED_RESPONSE_MESSAGE config options

v0.0.3:
=======

Features:

+ Return 429 (Too Many Requests) instead of 501 (Not Implemented) when rate limit is reached

v0.0.2:
=======

Features:

+ Added support for whitelist

v0.0.1:
=======

Features:

+ Initial release
