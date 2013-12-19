==========
Middleware
==========

If you're expecting to need to rate limit a large number of views, it's easier
to use the RatedMiddleware.  This also allows you to rate limit views from 3rd
party apps.

This will check each request to see if its url pattern name is in
settings.RATED_REALM_MAP.  This setting is a dict which maps url pattern names
to realms.

Example
=======

Here is an example of rate limiting all the views in the default auth password
reset pattern:

.. code-block:: python

    RATED_REALM_MAP = {
        'password_reset': 'password',
        'password_reset_done': 'password',
        'password_reset_confirm': 'password',
        'password_reset_complete': 'password',
    }

    RATED_REALMS = {
        'password': dict(limit=10, duration=10*60),
    }

