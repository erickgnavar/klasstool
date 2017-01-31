from django.test import TestCase, RequestFactory, tag
from django.urls import resolve

from ..views import HomeView


class HomeViewTestCase(TestCase):

    def setUp(self):
        self.view = HomeView.as_view()
        self.factory = RequestFactory()

    def test_match_expected_view(self):
        url = resolve('/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    @tag('html_render')
    def test_load_sucessful(self):
        request = self.factory.get('/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
