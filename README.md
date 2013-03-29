django-rated
============

A rate limiting middleware for Django

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
