from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.sessions.middleware import SessionMiddleware

from rest_framework.test import APIRequestFactory

from .profile.views import UsersViewSet


def add_middleware_to_request(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request


class TestUsersViewSetAsAdmin(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin, _ = User.objects.get_or_create(username='admin', is_superuser=True, is_staff=True)
        self.user1, _ = User.objects.get_or_create(username='alice')

    def test_should_display_user_list(self):
        admin, _ = User.objects.get_or_create(username='admin', is_superuser=True, is_staff=True)

        url = reverse("api:user-list")
        request = self.factory.get(url)
        request.user = self.admin

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = UsersViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200, "Admin should have access granted to the list of users")
        self.assertEqual(len(response.data), 2)

    def test_should_retrieve_any_profile(self):
        """
            This test will attempt to make request as admin to the profile of user 1
            It is expected that HTTP status code 200 will be returned.
        """
        admin, _ = User.objects.get_or_create(username='admin', is_superuser=True, is_staff=True)
        url = reverse("api:user-detail", kwargs={'pk': self.user1.pk})
        request = self.factory.get(url)
        request.user = self.admin

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = UsersViewSet.as_view({'get':'retrieve'})
        response = view(request, pk=self.user1.pk)
        self.assertEqual(response.status_code, 200)

    def test_should_create_new_user(self):
        """
            Administrator should be able to create new user
        """
        new_user = {
            'username': 'celine',
        }
        admin, _ = User.objects.get_or_create(username='admin', is_superuser=True, is_staff=True)
        url = reverse("api:user-list")
        request = self.factory.post(url, data=new_user)
        request.user = self.admin

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = UsersViewSet.as_view({'post': 'create'})
        response = view(request)
        failure_msg = "Admin should be able to create new user. "
        self.assertEqual(response.status_code, 201, failure_msg + str(response.data))
        user, created = User.objects.get_or_create(username='celine')

        failure_msg = "New user should have been created. "
        self.assertEqual(created, False, failure_msg)


class TestUsersViewSetAsUser(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user1, _ = User.objects.get_or_create(username='alice')
        self.user2, _ = User.objects.get_or_create(username='bob')

    def test_user_list_access_denied(self):
        url = reverse("api:user-list")
        request = self.factory.get(url)
        request.user = AnonymousUser()

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = UsersViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 403, "Users should not have access granted to the list of users")

    def test_user_retrieve_profile(self):
        """
            This test will attempt to make request as user 1 to the profile of user 1.
            It is expected that HTTP status code 200 will be returned.
        """
        url = reverse("api:user-detail", kwargs={'pk': self.user1.pk})
        request = self.factory.get(url)
        request.user = self.user1

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = UsersViewSet.as_view({'get':'retrieve'})
        response = view(request, pk=self.user1.pk)
        self.assertEqual(response.status_code, 200, "User should be able to access his/her profile")

    def test_user_retrieve_others_profile(self):
        """
            This test will attempt to make request as user 1 to the profile of user 2.
            It is expected that HTTP status code 403 (Forbidden) will be returned.
        """
        url = reverse("api:user-detail", kwargs={'pk': self.user2.pk})
        request = self.factory.get(url)
        request.user = self.user1

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = UsersViewSet.as_view({'get':'retrieve'})
        response = view(request, pk=self.user2.pk)
        self.assertEqual(response.status_code, 403, 'User should not have access to others profile')

    def test_post_method_as_user(self):
        """
            Non-administrative user should not be able to create new user
        """
        new_user = {
            'username': 'celine',
        }
        url = reverse("api:user-list")
        request = self.factory.post(url)
        request.user = self.user1

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = UsersViewSet.as_view({'post': 'create'})
        response = view(request, kwargs=new_user)

        failure_msg = "Non-admin should not create new user. "
        self.assertEqual(response.status_code, 403, failure_msg + str(response.data))

