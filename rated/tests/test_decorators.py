
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.test.utils import override_settings

from rated.decorators import rate_limit


class DecoratorTestCase(TestCase):

    def setUp(self):
        self.request = RequestFactory().get('/')
        # Clear old values

    @override_settings(
        RATED_REALMS={
            'default': dict(limit=1),
            'other': dict(limit=2),
        },
    )
    def test_rate_limit(self):
        @rate_limit
        def test_view(request):
            return HttpResponse('')

        resp = test_view(self.request)
        self.assertEqual(resp.status_code, 200)
        resp = test_view(self.request)
        self.assertEqual(resp.status_code, 429)

    @override_settings(
        RATED_REALMS={
            'default': dict(limit=1),
            'other': dict(limit=2),
        },
    )
    def test_other_realm(self):
        @rate_limit(realm='other')
        def test_view(request):
            return HttpResponse('1')

        resp = test_view(self.request)
        self.assertEqual(resp.status_code, 200)
        resp = test_view(self.request)
        self.assertEqual(resp.status_code, 200)
        resp = test_view(self.request)
        self.assertEqual(resp.status_code, 429)
