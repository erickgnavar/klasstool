from django.test import TestCase, RequestFactory, tag
from django.urls import resolve

from mixer.backend.django import mixer

from ..views import SessionPublicView


class SessionPublicViewTestCase(TestCase):

    def setUp(self):
        self.view = SessionPublicView.as_view()
        self.factory = RequestFactory()
        self.session = mixer.blend('courses.Session')

    def test_match_expected_view(self):
        url = resolve('/sessions/{}/'.format(self.session.id))
        self.assertEqual(url.func.__name__, self.view.__name__)

    @tag('html_render')
    def test_render_sucessful(self):
        response = self.client.get('/sessions/{}/'.format(self.session.id))
        self.assertEqual(response.status_code, 200)

    def test_load_sucessful(self):
        request = self.factory.get('/')
        response = self.view(request, session_id=self.session.id)
        self.assertEqual(response.status_code, 200)
