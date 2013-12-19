======
Realms
======

All views in the same realm are considered the same in terms of rate limiting.
This allows you to rate-limit access to a collection of views as a while, such
as an API or registration process.

Each realm can have its own timeout, limit, respones code/message, and
whitelist.  If not specified for a realm, these will fall back to the defaults.

Assigning Realms
================

There are two ways to assign a realm to a view.

rated_realm decorator
---------------------

The first is with the ``rated_realm`` decorator.

.. code-block:: python

    from rated.decorators import rated_realm

    # Mark a view as in the RATED_DEFAULT_REALM realm
    @rated_realm
    def first_view(request):
        ...

    @rated_realm(realm='neverwhere')
    def door(request):
        ...

It can also be used in url patterns, for instance with Class-Based Views

.. code-block:: python

    # Place view in default realm
    url(r'^$', rated_realm(myview))
    # Place view in a different realm
    url(r'^$', rated_realm(myview, realm='foo'))
    # Place CBV in a realm
    url(r'^$', rated_realm(MyView.as_view()))

rate_limit decorator
--------------------

Instead of adding the middleware, you can use the `rate_limit` decorator
directly on views.

.. code-block:: python

    from rated.decorators import rate_limit

    @rate_limit
    def first_view(request):
        ...

    @rate_limt(realm='other')
    def other_view(request):
        ...

For Class-Based Views, and django-nap Publishers, there is also
`rate_limit_method`, which works identically to `rate_limit`.


Realm map
---------

The second method is by using the RATED_REALM_MAP setting.  This allows you to
map url pattern names to realms.  This has two advantages:

1. It allows you to rate limit views in 3rd party realms without editing their
   code.
2. It lets you conditionally rate limit a view.

Config
======

Each Realm is configured by a dict with any of the following keys:

timeout::

    Duration (in seconds) for which the rate limiting applies.
    If not specified, this defaults to RATED_DEFAULT_TIMEOUT

limit::

    Maximum requets allowed from a single client in the timeout duration.
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
            'timeout': 60 * 30,
        },
        # Return a 501 response when limited
        'signup': dict(code=501),
    }

