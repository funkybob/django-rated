django-rated
============

A rate limiting middleware for Django

Introduction
============

rated allows you to limit the requests per hour a single client may attempt on views in 'realms' of your site.

You control which views are in which 'realm' by either decorating the view, or adding the url pattern into the realm map.

rated will keep track of how many requests, and when, a client has made and, if they've exceeded their limit, will return a 503 - Service Unavailable response.

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

RATED_REALMS:
    A dict of config dicts.
    The keys are realm names.
    The values are dicts containing overrides for 'limit' and 'timeout'.
    Default: {}

RATED_REALM_MAP:
    A mapping of url pattern names to realms.
    This allows you to apply limits to views in 3rd party apps.
    Default: {}

RATED_REDIS:
    Redis config settings.
