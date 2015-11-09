from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.core import serializers
from django.test import TestCase
from django.contrib.sessions.middleware import SessionMiddleware

from rest_framework.test import APIRequestFactory

from api.accounts.views import UserProfileViewSet, SkillsViewSet, EntityViewSet
from accounts.models import Skill, Entity, UserProfile, UserSkill

import json


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

        view = UserProfileViewSet.as_view({'get': 'list'})
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

        view = UserProfileViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.user1.pk)
        failure_msg = "Admin should be able to GET any profile. "
        self.assertEqual(response.status_code, 200, failure_msg + str(response.data))

    def test_should_create_new_user(self):
        """
            Administrator should be able to create new user
        """
        new_user = {
            'username': 'celine',
            'profile': None
        }
        admin, _ = User.objects.get_or_create(username='admin', is_superuser=True, is_staff=True)
        url = reverse("api:user-list")
        request = self.factory.post(url, data=new_user)
        request.user = self.admin

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = UserProfileViewSet.as_view({'post': 'create'})
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
        self.skill_haskell, _ = Skill.objects.get_or_create(name='Haskell', type=Skill.LANGUAGE)
        self.skill_erlang, _ = Skill.objects.get_or_create(name='Erlang', type=Skill.LANGUAGE)

        self.skill_json = serializers.serialize("json", [self.skill_erlang, self.skill_haskell])

    def test_should_not_list_users(self):
        url = reverse("api:user-list")
        request = self.factory.get(url)
        request.user = AnonymousUser()

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = UserProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 403, "Users should not have access granted to the list of users")

    def test_should_retrieve_profile(self):
        """
            This test will attempt to make request as user 1 to the profile of user 1.
            It is expected that HTTP status code 200 will be returned.
        """
        url = reverse("api:user-detail", kwargs={'pk': self.user1.pk})
        request = self.factory.get(url)
        request.user = self.user1

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = UserProfileViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.user1.pk)
        self.assertEqual(response.status_code, 200, "User should be able to access his/her profile")

    def test_should_not_retrieve_others_profile(self):
        """
            This test will attempt to make request as user 1 to the profile of user 2.
            It is expected that HTTP status code 403 (Forbidden) will be returned.
        """
        url = reverse("api:user-detail", kwargs={'pk': self.user2.pk})
        request = self.factory.get(url)
        request.user = self.user1

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = UserProfileViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.user2.pk)
        self.assertEqual(response.status_code, 403, 'User should not have access to others profile')

    def test_should_not_create_user(self):
        """
            Non-administrative user should not be able to create new user
        """
        new_user = {
            'username': 'celine',
        }
        url = reverse("api:user-list")
        request = self.factory.post(url, data=new_user)
        request.user = self.user1

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = UserProfileViewSet.as_view({'post': 'create'})
        response = view(request, kwargs=new_user)

        failure_msg = "Non-admin should not create new user. "
        self.assertEqual(response.status_code, 403, failure_msg + str(response.data))

    def test_should_update_profile(self):
        """
        User should be able to update his profile
        """
        update_data = {
            'profile': {
                'skills': [self.skill_json]
            }
        }
        update_data_json = json.dumps(update_data)
        url = reverse("api:user-detail", kwargs={'pk': self.user1.pk})
        request = self.factory.patch(url, data=update_data_json)
        request.user = self.user1

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = UserProfileViewSet.as_view({'patch': 'partial_update'})
        response = view(request, pk=self.user1.pk)
        failure_msg = "User should be able to update his/her profile. "
        self.assertEqual(response.status_code, 200, failure_msg + str(response.data))

        u = User.objects.get(pk=self.user1.pk)
        for s in u.profile.skills:
            print(str(s))

    def test_should_not_update_profile(self):
        """
        User should not be able to update others profile
        """
        raise NotImplementedError


class TestSkillsViewSet(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user1, _ = User.objects.get_or_create(username='alice')
        self.new_skill = {
            "name": "Haskell",
            "type": Skill.LANGUAGE
        }

    def test_should_list_skills(self):
        url = reverse("api:skill-list")
        request = self.factory.get(url)
        request.user = AnonymousUser()

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = SkillsViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200, "Anybody should be able to list skills")

    def test_should_create_skill(self):
        url = reverse("api:skill-list")

        request = self.factory.post(url, data=self.new_skill)
        request.user = self.user1

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = SkillsViewSet.as_view({'post': 'create'})
        response = view(request)

        failure_msg = "User should be able to add skill. "
        self.assertEqual(response.status_code, 201, failure_msg + str(response.data))

    def test_should_not_create_skill(self):
        url = reverse("api:skill-list")

        request = self.factory.post(url, data=self.new_skill)
        request.user = AnonymousUser()

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = SkillsViewSet.as_view({'post': 'create'})
        response = view(request)

        failure_msg = "Anonymous user should not be able to create skill. "
        self.assertEqual(response.status_code, 403, failure_msg + str(response.data))


class TestEntityAsAdmin(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user1, _ = User.objects.get_or_create(username='alice')
        self.user1profile, _ = UserProfile.objects.get_or_create(user=self.user1, is_employer=False)
        self.admin, _ = User.objects.get_or_create(username='admin', is_superuser=True, is_staff=True)
        self.new_entity_data = {
            'city': 'Wroclaw',
            'country': 'Poland',
        }
        self.skill1, _ = Skill.objects.get_or_create(name='Scheme', type=Skill.LANGUAGE)
        self.skill1data = {
            'name': 'Scheme',
            'type': Skill.LANGUAGE,
            'level': UserSkill.BEGINNER
        }

        self.new_skills_data = [
            {
                'level': UserSkill.ADVANCED,
                'name': 'Erlang',
                'type': Skill.LANGUAGE
            },
            {
                'level': UserSkill.INTERMEDIATE,
                'name': 'Python',
                'type': Skill.LANGUAGE
            }
        ]

    def test_should_create_entity(self):
        url = reverse('api:entity-list', kwargs={'parent_lookup_profile': 'alice'})
        request = self.factory.post(url, data=json.dumps(self.new_entity_data), content_type='application/json')
        request.user = self.admin
        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = EntityViewSet.as_view({'post': 'create'})
        response = view(request, parent_lookup_profile='alice')

        failure_msg = "Admin should be able to add entity to user. "
        self.assertEqual(response.status_code, 201, failure_msg + str(response.data))
        Entity.objects.all().delete()

    def test_should_create_entity_and_skills(self):
        url = reverse('api:entity-list', kwargs={'parent_lookup_profile': 'alice'})

        self.new_entity_data['skills'] = self.new_skills_data
        request = self.factory.post(url, data=json.dumps(self.new_entity_data), content_type='application/json')
        request.user = self.admin
        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = EntityViewSet.as_view({'post': 'create'})
        response = view(request, parent_lookup_profile='alice')

        failure_msg = "Admin should be able to add entity to user. "
        self.assertEqual(response.status_code, 201, failure_msg + str(response.data))

        failure_msg = "User skills should've been added. "
        self.assertEqual(len(response.data['skills']), len(self.new_skills_data), failure_msg + str(response.data))
        Skill.objects.all().delete()

    def test_should_create_entity_and_skill_already_exists(self):
        url = reverse('api:entity-list', kwargs={'parent_lookup_profile': 'alice'})

        # New entity should contain skills from JSON + existing skill
        self.new_entity_data['skills'] = self.new_skills_data+[self.skill1data]
        request = self.factory.post(url, data=json.dumps(self.new_entity_data), content_type='application/json')
        request.user = self.admin
        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        view = EntityViewSet.as_view({'post': 'create'})
        response = view(request, parent_lookup_profile='alice')

        failure_msg = "Admin should be able to add entity to user. "
        self.assertEqual(response.status_code, 201, failure_msg + str(response.data))

        failure_msg = "User skills should've been added. "
        self.assertEqual(len(response.data['skills']), len(self.new_entity_data['skills']), failure_msg + str(response.data))  # noqa
        Skill.objects.all().delete()
