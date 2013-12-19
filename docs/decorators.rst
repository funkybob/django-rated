==========
Decorators
==========

If you want to be very selective in where you rate limit, or only have a few
views you want to limit, the decorator approach is probably best.

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

The `rate_limit_method` decorator
=================================

This decorator allows you to apply rate-limiting on any view-like method in a
class-based view.  That is, any method that is passed request, and expected to
return a HttpResponse class.

At its simples, it can be used to decorate the `dispatch` method of any CBV.
However, it can also be used to decorate the `get` or `post` method, allowing
you to rate limit based on HTTP verb.

Additionally, if you are using ``django-nap``, this can be used to rate-limit
individual handler methods.

Example
-------

Here's an example of rate-liming only posting of new support request tickets:

.. code-block:: python

    class CreateRequestView(CreateView):
        model = SupportRequest

        @rate_limit_method(realm='support')
        def post(self, request, *args, **kwargs):
            return super(CreateRequestView, self).post(request, *args, **kwargs)


