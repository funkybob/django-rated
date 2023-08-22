==========
Decorators
==========

The `rate_limit` decorator
==========================

Example
-------

Here's an example of rate-limiting at view definition:

.. code-block:: python

    from rated.decorators import rate_limit

    # This will place the view in the RATED_DEFAULT_REALM realm
    @rate_limit
    def first_view(request, ...):

    # This will place the view in the 'special' realm
    @rate_limit(realm='special')
    def special_view(request, ...):

Alternatively, you can decorate views in your url patterns:

.. code-block:: python

    urlpatterns = patterns('',
        url(r'^special/$', rate_limit(special_view, 'special')),
        url(r'^$', rate_limit(CBView.as_view())),
    )
