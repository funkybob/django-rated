from time import sleep

from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.test.utils import override_settings

import redis

from rated.decorators import rate_limit, POOL


class DecoratorTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.redis = redis.Redis(connection_pool=POOL)

    def setUp(self):
        self.request = RequestFactory().get('/')
        self.redis.flushdb()

    @override_settings(
        RATED_REALMS={
            'default': {'limit': 1},
            'other': {'limit': 2},
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
            'default': {
                'limit': 1,
                'duration': 1,
            },
        },
    )
    def test_limit_expires(self):
        @rate_limit
        def test_view(request):
            return HttpResponse('')

        resp = test_view(self.request)
        self.assertEqual(resp.status_code, 200)
        resp = test_view(self.request)
        self.assertEqual(resp.status_code, 429)

        sleep(2)

        resp = test_view(self.request)
        self.assertEqual(resp.status_code, 200)

    @override_settings(
        RATED_REALMS={
            'default': {'limit': 1},
            'other': {'limit': 2},
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
