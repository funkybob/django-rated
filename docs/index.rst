.. django-rated documentation master file, created by
   sphinx-quickstart on Thu Dec  5 11:05:37 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-rated's documentation!
========================================

Rated is a multi-domain rate limiting middleware for Django.

Quickstart
----------

1. Add 'rated.middleware.RatedMiddleware' to your settings.MIDDLEWARE_CLASSES

2. Set your default limits:

.. code-block:: python

   RATED_DEFAULT_REALM = 'default'
   # Duration over which we count requests
   RATED_DEFAULT_TIMEOUT = 60 * 60
   # Maximum number of requests in TIMEOUT period
   RATED_DEFAULT_LIMIT = 100

3. Mark views as belonging to a rate limited realm.

.. code-block:: python

   @rated_realm
   def myview(request...


Contents:
---------

.. toctree::
   :maxdepth: 2

   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

