django-rated
============
[![Downloads](https://pypip.in/d/django-rated/badge.png)](https://crate.io/package/django-rated)
[![Version](https://pypip.in/v/django-rated/badge.png)](https://crate.io/package/django-rated)
[![Build Status](https://secure.travis-ci.org/funkybob/django-rated.png?branch=master)](http://travis-ci.org/funkybob/django-rated)


A rate limiting decorators for Django

Introduction
============

`rated`` allows you to limit request rates a single client may attempt on views in 'realms' of your site.

You control which views are in which 'realm' by either decorating the view, or adding the url pattern into the realm map.

`rated` will keep track of how many requests, and when, a client has made and, if they've exceeded their limit, will return a configurable response -- `503 - Service Unavailable` by default.

Installing
==========

Decorate your views:

```py
@rate_limit('myrealm')
def myview(request):
```

Configuring
===========

Next, configure your realms.

This is done by defining them in the RATED_REALMS setting.  This is a dict where the keys are realm names, and the values are dicts of configs.

A realm config may contain any of the following keys.  Any omitted fall back to the defaults from the settings below.

    allowed:  A list of IPs to exclude from rate limiting.
    duration:   Time after which any requests are forgotten
    limit:      Number of requests before limiting is applied.
    code:       HTTP Status code to use when limiting is applied.
    message:    Response content to return when limiting is applied.

If you're planning to put all limited views into the one realm, you don't need to define RATED_REALMS - the defaults will be used instead.

Assign Realms
=============

There are three ways to apply rate limits.  Either decorate the view directly, add a realm with the same url pattern name, or map the url pattern name to a realm.

You can add mark a view as in the default realm simply:

```py
from rated.decorators import rate_limit

@rate_limit
def myview(...)
```

To add it to a specific realm:

```py
@rated_realm(realm='other')
def myview(...)
```

Otherwise, if the url pattern is named, and the name matches a realm name, it will be considered part of that realm.  There is also the RATED_REALM_MAP, which will map url pattern names to realm names.  The url pattern name is always mapped through here.

Settings
========

RATED_DEFAULT_REALM:

    The default realm to put views into.
    Default: 'default'

RATED_DEFAULT_TIMEOUT:

    How long an access history persists with no accesses.
    Default: 1 hour

RATED_DEFAULT_LIMIT:

    Limit of how many requests an individual client is permitted per hour.
    Default: 100

RATED_RESPONSE_CODE:

    HTTP Status code to return when a request is limited.
    Default: 429

RATED_RESPONSE_MESSAGE:

    Content to include in response when a request is limited.
    Default: ''

RATED_REALMS:

    A dict of config dicts.
    The keys are realm names.
    The values are dicts containing overrides for 'limit', 'timeout' and 'allowed'.
    Default: {}

RATED_REDIS:

    Redis config settings.
    These will be passed directly to create a redis.ConnectionPool instance.

RATED_DEFAULT_ALLOWED:

    A list of IPs which are exempt from rate limiting.
