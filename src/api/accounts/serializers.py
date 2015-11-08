from django.contrib.auth.models import User

from rest_framework.reverse import reverse
from rest_framework import serializers

from accounts.models import UserProfile, Skill, UserSkill, Entity


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill


class UserSkillSerializer(serializers.ModelSerializer):
    skill = serializers.CharField(source='skill.name')
    skill_type = serializers.CharField(source='skill.type')

    class Meta:
        fields = ('skill', 'skill_type', 'level')
        model = UserSkill


class EntitySerializer(serializers.ModelSerializer):
    skills = UserSkillSerializer(many=True)
    links = serializers.SerializerMethodField()

    class Meta:
        model = Entity
        fields = ('city', 'country', 'skills', 'links')

    def get_links(self, obj):
        request = self.context['request']
        view = self.context['view']
        entity_relative_url = reverse('api:entity-detail',
                                      kwargs={
                                          'parent_lookup_profile': view.kwargs['parent_lookup_profile'],
                                          'pk': obj.pk
                                      })
        entity_absolute_url = request.build_absolute_uri(entity_relative_url)
        return {
            'self': entity_absolute_url
        }

    def create(self, validated_data):
        username = self.context['view'].kwargs['parent_lookup_profile']
        user = User.objects.get(username=username)
        skills = validated_data.pop('skills')
        entity = Entity(**validated_data)
        entity.user_profile = user.userprofile
        self.assign_skills(entity, skills)
        entity.save()
        return entity

    def assign_skills(self, entity, skills):
        for skill_data in skills:
            from pprint import pprint
            pprint(skill_data)
            skill = Skill.objects.get_or_create(name=skill_data['skill'], type=skill_data['skill_type'])
            UserSkill.objects.get_or_create(level=skill_data['level'], skill=skill, entity=entity)


class UserProfileSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('is_employer', 'links')

    def get_links(self, obj):
        request = self.context['request']
        entity_relative_url = reverse('api:entity-list',
                                   kwargs={
                                       'parent_lookup_profile': obj.user.username
                                   })
        entity_absolute_url = request.build_absolute_uri(entity_relative_url)
        return {
            'entities': entity_absolute_url
        }

    def create(self, validated_data):
        user = validated_data.pop('user')
        username = user.get('username', None)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            message = "User {} does not exist.".format(username)
            raise serializers.ValidationError(message)

        return UserProfile.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.update(**validated_data)
        instance.save()
