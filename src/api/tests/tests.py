from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.core import serializers
from django.test import TestCase
from django.contrib.sessions.middleware import SessionMiddleware

from rest_framework.test import APIRequestFactory, force_authenticate

from api.accounts.views import UserProfileViewSet, SkillsViewSet, EntityViewSet
from accounts.models import Skill, Entity, UserProfile, UserSkill

import json
import pprint

factory = APIRequestFactory()


def format_failure_message(msg, additional_data):
    data_formatted = pprint.pformat(additional_data, indent=4)
    output = msg + '\n\n' + data_formatted
    return output


class TestUserProfileViewSetAsAdmin(TestCase):
    fixtures = ['users', 'user_profile']

    def setUp(self):
        self.admin = User.objects.get(username='admin')
        self.user1 = User.objects.get(username='alice')
        self.user2 = User.objects.get(username='bob')

    def test_should_list_profiles(self):
        """
            Admin should be able to list all available profiles
        """
        url = reverse("api:user-profile-list")
        request = factory.get(url)
        force_authenticate(request, user=self.admin)

        view = UserProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        
        failure_msg = "Admin should have access granted to the list of users' profiles."
        self.assertEqual(response.status_code, 200, format_failure_message(failure_msg, response.data))
        self.assertEqual(len(response.data), UserProfile.objects.all().count())

    def test_should_retrieve_profile(self):
        """
            This test will attempt to make request as admin to the profile of user alice
            It is expected that HTTP status code 200 will be returned.
        """
        url = reverse("api:user-profile-detail", kwargs={'user__username': self.user1.username})
        request = factory.get(url)
        force_authenticate(request, user=self.admin)

        view = UserProfileViewSet.as_view({'get': 'retrieve'})
        response = view(request, user__username=self.user1.username)
        
        failure_msg = "Admin should be able to GET any profile."
        self.assertEqual(response.status_code, 200, format_failure_message(failure_msg, response.data))

    def test_should_create_profile(self):
        """
            Administrator should be able to create new profile for an existing user
        """
        new_profile = {
            "is_employer": False,
            "user": self.user2.username
        }

        url = reverse("api:user-profile-list")
        request = factory.post(url, data=new_profile)
        force_authenticate(request, user=self.admin)

        view = UserProfileViewSet.as_view({'post': 'create'})
        response = view(request)
        
        failure_msg = "Admin should be able to create new profile for an existing user."
        self.assertEqual(response.status_code, 201, format_failure_message(failure_msg, response.data))


class TestUserProfileViewSetAsUser(TestCase):
    fixtures = ['users', 'user_profile']

    def setUp(self):
        self.user1 = User.objects.get(username='alice')
        self.user2 = User.objects.get(username='bob')

    def test_should_not_list_users(self):
        url = reverse("api:user-profile-list")
        request = factory.get(url)
        force_authenticate(request, user=AnonymousUser())

        view = UserProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        
        failure_msg = "Users should not have access granted to the list of users"
        self.assertEqual(response.status_code, 403, failure_msg)

    def test_should_retrieve_profile(self):
        """
            This test will attempt to make request as user alice to the profile of user alice.
            It is expected that HTTP status code 200 will be returned.
        """
        url = reverse("api:user-profile-detail", kwargs={'user__username': self.user1.username})
        request = factory.get(url)
        force_authenticate(request, user=self.user1)

        view = UserProfileViewSet.as_view({'get': 'retrieve'})
        response = view(request, user__username=self.user1.username)
        
        failure_msg = "User should be able to access his/her profile"
        self.assertEqual(response.status_code, 200, failure_msg)

    def test_should_not_retrieve_others_profile(self):
        """
            This test will attempt to make request as user bob to the profile of user alice.
            It is expected that HTTP status code 403 (Forbidden) will be returned.
        """
        url = reverse("api:user-profile-detail", kwargs={'user__username': self.user1.username})
        request = factory.get(url)
        force_authenticate(request, user=self.user2)

        view = UserProfileViewSet.as_view({'get': 'retrieve'})
        response = view(request, user__username=self.user1.username)
        
        failure_msg = 'User should not have access to a profile belonging to someone else.'
        self.assertEqual(response.status_code, 403, failure_msg)

    def test_should_not_create_profile(self):
        """
            User alice should not be able to create a profile for user bob
        """
        new_profile = {
            "is_employer": False,
            "user": self.user2.username
        }

        url = reverse("api:user-profile-list")
        request = factory.post(url, data=new_profile)
        force_authenticate(request, user=self.user1)

        view = UserProfileViewSet.as_view({'post': 'create'})
        response = view(request)

        failure_msg = "User should not be able to create a profile for someone else."
        self.assertEqual(response.status_code, 403, format_failure_message(failure_msg, response.data))

    def test_should_create_profile(self):
        """
            User bob should be able to create himself a profile
        """
        new_profile = {
            "is_employer": False,
            "user": self.user2.username
        }

        url = reverse("api:user-profile-list")
        request = factory.post(url, data=new_profile)
        force_authenticate(request, user=self.user2)

        view = UserProfileViewSet.as_view({'post': 'create'})
        response = view(request)

        failure_msg = "User should be able to create itself a profile."
        self.assertEqual(response.status_code, 201, format_failure_message(failure_msg, response.data))

    def test_should_update_profile(self):
        """
        User should be able to update his profile
        """
        is_employer = self.user1.userprofile.is_employer
        update_data = {
            'is_employer': not is_employer
        }

        url = reverse("api:user-profile-detail", kwargs={'user__username': self.user1.username})
        request = factory.patch(url, data=update_data)
        force_authenticate(request, user=self.user1)

        view = UserProfileViewSet.as_view({'patch': 'partial_update'})
        response = view(request, user__username=self.user1.username)
        
        failure_msg = "User should be able to update his/her profile."
        self.assertEqual(response.status_code, 200, format_failure_message(failure_msg, response.data))

    def test_should_not_update_profile(self):
        """
        User should not be able to update others profile
        """
        is_employer = self.user1.userprofile.is_employer
        update_data = {
            'is_employer': not is_employer
        }

        url = reverse("api:user-profile-detail", kwargs={'user__username': self.user1.username})
        request = factory.patch(url, data=update_data)
        force_authenticate(request, user=self.user2)

        view = UserProfileViewSet.as_view({'patch': 'partial_update'})
        response = view(request, user__username=self.user1.username)

        failure_msg = "User should not be able to update others profile."
        self.assertEqual(response.status_code, 403, format_failure_message(failure_msg, response.data))


class TestSkillsViewSet(TestCase):
    fixtures = ['users']

    def setUp(self):
        self.user1 = User.objects.get(username='alice')
        self.new_skill = {
            "name": "Haskell",
            "type": Skill.LANGUAGE
        }

    def test_should_list_skills(self):
        url = reverse("api:skill-list")
        request = factory.get(url)
        force_authenticate(request, user=AnonymousUser())

        view = SkillsViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200, "Anybody should be able to list skills")

    def test_should_create_skill(self):
        url = reverse("api:skill-list")

        request = factory.post(url, data=self.new_skill)
        force_authenticate(request, user=self.user1)

        view = SkillsViewSet.as_view({'post': 'create'})
        response = view(request)

        failure_msg = "User should be able to add skill. "
        self.assertEqual(response.status_code, 201, format_failure_message(failure_msg, response.data))

    def test_should_not_create_skill(self):
        url = reverse("api:skill-list")

        request = factory.post(url, data=self.new_skill)
        force_authenticate(request, user=AnonymousUser())

        view = SkillsViewSet.as_view({'post': 'create'})
        response = view(request)

        failure_msg = "Anonymous user should not be able to create skill. "
        self.assertEqual(response.status_code, 403, format_failure_message(failure_msg, response.data))


class TestEntityViewSetAsAdmin(TestCase):
    fixtures = ['users', 'skills', 'user_profile']

    def setUp(self):
        self.admin = User.objects.get(username='admin')
        self.user1 = User.objects.get(username='alice')
        self.skill1 = Skill.objects.get(name='Python')
        self.number_of_skills = Skill.objects.all().count()
        self.user1_profile = UserProfile.objects.get(user=self.user1)
        
        self.new_entity_data = {
            'city': 'Wroclaw',
            'country': 'Poland',
        }
        self.new_entity_data2 = {
            'city': 'Paris',
            'country': 'France',
        }

        self.new_skills_data = [
            {
                'level': UserSkill.ADVANCED,
                'name': 'Scheme',  # NOTICE: This skill must not be in fixture
                'type': Skill.LANGUAGE
            },
            {
                'level': UserSkill.INTERMEDIATE,
                'name': 'Python',
                'type': Skill.LANGUAGE
            }
        ]

    def test_should_create_entity(self):
        """
        Admin should be able to create an entity for a user.
        """
        url = reverse('api:entity-list', kwargs={'parent_lookup_profile': 'alice'})
        request = factory.post(url, data=json.dumps(self.new_entity_data), content_type='application/json')
        force_authenticate(request, user=self.admin)

        view = EntityViewSet.as_view({'post': 'create'})
        response = view(request, parent_lookup_profile='alice')

        failure_msg = "Admin should be able to add entity to user. "
        self.assertEqual(response.status_code, 201, format_failure_message(failure_msg, response.data))

    def test_should_create_entity_and_skills(self):
        """
            It should be possible to create the entity for Alice.
            NOTICE: In fixture it is the bob who doesn't have user profile
        """
        url = reverse('api:entity-list', kwargs={'parent_lookup_profile': 'alice'})

        self.new_entity_data['skills'] = self.new_skills_data
        request = factory.post(url, data=json.dumps(self.new_entity_data), content_type='application/json')
        force_authenticate(request, user=self.admin)

        view = EntityViewSet.as_view({'post': 'create'})
        response = view(request, parent_lookup_profile='alice')

        failure_msg = "Admin should be able to add entity to user. "
        self.assertEqual(response.status_code, 201, format_failure_message(failure_msg, response.data))

        failure_msg = "User skills should've been added. "
        self.assertEqual(len(response.data['skills']),
                         len(self.new_skills_data),
                         format_failure_message(failure_msg, response.data))

        failure_msg = "New skill should have been created."
        self.assertEqual(Skill.objects.all().count(), self.number_of_skills + 1, failure_msg)

    def test_should_retrieve_entity(self):
        """
        Admin should be able to retrieve entity.
        """
        entity, _ = Entity.objects.get_or_create(user_profile=self.user1_profile, **self.new_entity_data2)

        url = reverse('api:entity-detail', kwargs={'parent_lookup_profile': self.user1.username, 'pk': entity.pk})
        request = factory.get(url, data=self.new_entity_data)
        force_authenticate(request, user=self.admin)

        view = EntityViewSet.as_view({'get': 'retrieve'})
        response = view(request, parent_lookup_profile='alice', pk=entity.pk)

        failure_msg = "Admin should be able to retrieve user entity."
        self.assertEqual(response.status_code, 200, format_failure_message(failure_msg, response.data))

    def test_should_update_entity(self):
        """
        Admin should be able to update user entity.
        """
        entity, _ = Entity.objects.get_or_create(user_profile=self.user1_profile, **self.new_entity_data2)
        url = reverse('api:entity-detail', kwargs={'parent_lookup_profile': self.user1.username, 'pk': entity.pk})
        request = factory.put(url, data=self.new_entity_data)
        force_authenticate(request, user=self.admin)

        view = EntityViewSet.as_view({'put': 'update'})
        response = view(request, parent_lookup_profile='alice', pk=entity.pk)

        failure_msg = "Admin should be able to update user entity."
        self.assertEqual(response.status_code, 200, format_failure_message(failure_msg, response.data))
        self.assertNotEqual(response.data['city'],
                         self.new_entity_data2['city'],
                         format_failure_message(failure_msg, response.data))
        entity.delete()


class TestEntityViewSetAsUser(TestCase):
    fixtures = ['users', 'skills', 'user_profile']

    def setUp(self):
        self.user1 = User.objects.get(username='alice')
        self.skill1 = Skill.objects.get(name='Python')
        self.number_of_skills = Skill.objects.all().count()
        self.user1_profile = UserProfile.objects.get(user=self.user1)

        self.new_entity_data = {
            'city': 'Wroclaw',
            'country': 'Poland',
        }
        self.new_entity_data2 = {
            'city': 'Paris',
            'country': 'France',
        }

        self.new_skills_data = [
            {
                'level': UserSkill.ADVANCED,
                'name': 'Scheme',  # NOTICE: This skill must not be in fixture
                'type': Skill.LANGUAGE
            },
            {
                'level': UserSkill.INTERMEDIATE,
                'name': 'Python',
                'type': Skill.LANGUAGE
            }
        ]

    def test_should_create_entity_and_skills(self):
        """
            User Alice should be able to create herself an entity with skills.
            NOTICE: In fixture it is Bob who doesn't have user profile
        """
        url = reverse('api:entity-list', kwargs={'parent_lookup_profile': 'alice'})

        self.new_entity_data['skills'] = self.new_skills_data
        request = factory.post(url, data=json.dumps(self.new_entity_data), content_type='application/json')
        force_authenticate(request, user=self.user1)

        view = EntityViewSet.as_view({'post': 'create'})
        response = view(request, parent_lookup_profile='alice')

        failure_msg = "Admin should be able to add entity to user. "
        self.assertEqual(response.status_code, 201, format_failure_message(failure_msg, response.data))

        failure_msg = "User skills should've been added. "
        self.assertEqual(len(response.data['skills']),
                         len(self.new_skills_data),
                         format_failure_message(failure_msg, response.data))

        failure_msg = "New skill should have been created."
        self.assertEqual(Skill.objects.all().count(), self.number_of_skills + 1, failure_msg)

    def test_should_retrieve_entity(self):
        """
        User alice should be able to retrieve her entity
        """
        entity, _ = Entity.objects.get_or_create(user_profile=self.user1_profile, **self.new_entity_data2)

        url = reverse('api:entity-detail', kwargs={'parent_lookup_profile': self.user1.username, 'pk': entity.pk})
        request = factory.get(url, data=self.new_entity_data)
        force_authenticate(request, user=self.user1)

        view = EntityViewSet.as_view({'get': 'retrieve'})
        response = view(request, parent_lookup_profile='alice', pk=entity.pk)

        failure_msg = "Admin should be able to retrieve user entity."
        self.assertEqual(response.status_code, 200, format_failure_message(failure_msg, response.data))

    def test_should_update_entity(self):
        """
        User alice should be able to update her entity
        """
        entity, _ = Entity.objects.get_or_create(user_profile=self.user1_profile, **self.new_entity_data2)
        url = reverse('api:entity-detail', kwargs={'parent_lookup_profile': self.user1.username, 'pk': entity.pk})
        request = factory.put(url, data=self.new_entity_data)
        force_authenticate(request, user=self.user1)

        view = EntityViewSet.as_view({'put': 'update'})
        response = view(request, parent_lookup_profile='alice', pk=entity.pk)

        failure_msg = "Admin should be able to update user entity."
        self.assertEqual(response.status_code, 200, format_failure_message(failure_msg, response.data))
        self.assertNotEqual(response.data['city'],
                         self.new_entity_data2['city'],
                         format_failure_message(failure_msg, response.data))
        entity.delete()

    def test_should_not_retrieve_entity(self):
        """
        User bob shouldn't be able to retrieve alice entity
        """
        raise NotImplementedError

    def test_should_not_update_entity(self):
        """
        User bob shouldn't be able to update alice entity
        """
        raise NotImplementedError

    def test_should_not_create_entity(self):
        """
        User bob shouldn't be able to create an entity for alice
        """
        raise NotImplementedError
