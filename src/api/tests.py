from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from .profile.views import ProfileViewSet


def add_middleware_to_response(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request


class APIUserEndpoint(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User.objects.get_or_create(username='alice')
        User.objects.get_or_create(username='bob')

    def test_user_list_access_granted(self):
        url = reverse("api:users")
        request = self.factory.get(url)
        response = ProfileViewSet.as_view(request)
        self.assertEquals(response.count, 2)

    def test_user_list_access_denied(self):
        pass
