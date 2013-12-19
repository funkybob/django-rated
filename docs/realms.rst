======
Realms
======

All views in the same realm are considered equally in terms of rate limiting.
This allows you to rate-limit access to a collection of views as a whole, such
as an API or registration process.

Each realm can have its own duration, limit, respones code/message, and
whitelist.  If not specified for a realm, these will fall back to the defaults.

Config
======

Each Realm is configured by a dict with any of the following keys:

duration::

    Duration (in seconds) for which the rate limiting applies.
    If not specified, this defaults to RATED_DEFAULT_DURATION

limit::

    Maximum requets allowed from a single client in the duration.
    If not specified, this defaults to RATED_DEFAULT_LIMIT

code::

    The HTTP Status code to use when a request is rate limited.
    If not specified, this defaults to RATED_DEFAULT_CODE

message::

    The content to include in responses for rate limited requests.
    If not specified, this defaults to RATED_DEFAULT_MESSAGE

whitelist::

    A list of IPs of clients exempt from rate limiting in this realm.
    If not specified, this defaults to RATED_DEFAULT_WHITELIST.

Example
-------

.. code-block:: python

    RATED_REALMS = {
        # Limit access to the 'user_api' Realm to 10 requests in the last half hour.
        'user_api': {
            'limit': 10,
            'duration': 60 * 30,
        },
        # Return a 501 response when limited
        'signup': dict(code=501),
    }

