from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

from .profile.views import ProfileViewSet


def add_middleware_to_request(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request


class APIUserEndpoint(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1, _ = User.objects.get_or_create(username='alice')
        self.user2, _ = User.objects.get_or_create(username='bob')

    def test_user_list_access_granted(self):
        admin, _ = User.objects.get_or_create(username='admin', is_superuser=True, is_staff=True)

        url = reverse("api:user-list")
        request = self.factory.get(url)
        request.user = admin

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = ProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_user_list_access_denied(self):
        url = reverse("api:user-list")
        request = self.factory.get(url)
        request.user = AnonymousUser()

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = ProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 401, "Non-administrative accounts should not have the access granted")

    def test_user_retrieve_profile(self):
        url = reverse("api:user-detail") #TODO Pass user pk
        request = self.factory.get(url)
        request.user = self.user1

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = ProfileViewSet.as_view({'get':'retrieve'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_user_retrieve_others_profile(self):
        pass
