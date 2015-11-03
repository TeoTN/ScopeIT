from django.contrib.auth.models import User
from django.core.exceptions import FieldDoesNotExist

from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from app_profile.models import UserProfile, Skill, UserSkill, ProfessionalProfile


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill


class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill


class ProfessionalProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    links = serializers.SerializerMethodField()

    class Meta:
        model = ProfessionalProfile
        fields = ('city', 'country', 'skills', 'links')

    def get_links(self, obj):
        request = self.context['request']
        professional_url = reverse('api:professional-profile-detail',
                                   kwargs={
                                       'parent_lookup_profile': obj.user_profile.user.username,
                                       'pk': obj.pk
                                   })
        professional_absolute_url = request.build_absolute_uri(professional_url)
        return {
            'self': professional_absolute_url
        }


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    links = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('username', 'is_employer', 'links')

    def get_links(self, obj):
        request = self.context['request']
        professional_url = reverse('api:professional-profile-list',
                                   kwargs={
                                       'parent_lookup_profile': obj.user.username
                                   })
        professional_absolute_url = request.build_absolute_uri(professional_url)
        return {
            'professional_profiles': professional_absolute_url
        }
