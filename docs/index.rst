.. django-rated documentation master file, created by
   sphinx-quickstart on Thu Dec  5 11:05:37 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

======================================
django-rated - Rate Limiting made easy
======================================

.. image:: https://travis-ci.org/funkybob/django-rated.png
           :target: https://secure.travis-ci.org/funkybob/django-rated.png?branch=master

.. image:: https://pypip.in/d/django-rated/badge.png
           :target: https://crate.io/packages/django-rated

.. image:: https://pypip.in/v/django-rated/badge.png
           :target: https://crate.io/packages/django-rated

Rated provides fine-grained rate limiting controls for Django.

It allows you do define multiple "realms", each with its own limit, allowed list,
and responses.

There are two mechanisms, which can be used individually, or combined:

1. Middlware that lets you assign url patterns into realms.
2. Decorators that let you rate limit views individually.

----------
Quickstart
----------

Middleware
----------

1. Add 'rated.middleware.RatedMiddleware' to your settings.MIDDLEWARE_CLASSES

2. Set your default limits:

.. code-block:: python

   RATED_DEFAULT_REALM = 'default'
   # Duration over which we count requests
   RATED_DEFAULT_DURATION = 60 * 60
   # Maximum number of requests in DURATION period
   RATED_DEFAULT_LIMIT = 100

3. Assign URL patterns to realms:

.. code-block:: python

    RATED_REALMS_MAP = {
        'index': 'default',
        'important_view': 'default',
    }

Decorators
----------

1. Set your limits

.. code-block:: python

   RATED_DEFAULT_REALM = 'default'
   # Duration over which we count requests
   RATED_DEFAULT_DURATION = 60 * 60
   # Maximum number of requests in DURATION period
   RATED_DEFAULT_LIMIT = 100

2. Decorate your views

.. code-block:: python

    @rate_limit
    def my_view(request, ...)

    @rate_limit(realm='special')
    def special_view(request, ...)

Contents:
---------

.. toctree::
   :maxdepth: 2

   realms
   middleware
   decorators
   settings
   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

