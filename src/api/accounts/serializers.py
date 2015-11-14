from django.contrib.auth.models import User

from rest_framework.reverse import reverse
from rest_framework import serializers

from accounts.models import UserProfile, Skill, UserSkill, Entity


class UserSkillSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='skill.name')
    type = serializers.CharField(source='skill.type')

    class Meta:
        model = UserSkill
        fields = ('profile', 'name', 'type', 'level')

    def create(self, validated_data):
        # Get or create skills
        skills_data = validated_data.pop('skill', None)
        try:
            skill = Skill.objects.get(name=skills_data['name'])
        except Skill.DoesNotExist:
            skill_serializer = SkillSerializer(data=skills_data)
            skill_serializer.is_valid(raise_exception=True)
            skill = skill_serializer.save()

        validated_data['skill'] = skill
        userskill = super(UserSkillSerializer, self).create(validated_data)

        return userskill


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'type')
        model = Skill


class EntitySerializer(serializers.ModelSerializer):
    skills = UserSkillSerializer(source='userskill_set', many=True, read_only=True)
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
        # Get user
        username = self.context['view'].kwargs['parent_lookup_profile']
        user = User.objects.get(username=username)

        # Create entity
        validated_data.pop("skills", None)
        entity = Entity(**validated_data)
        entity.user_profile = user.userprofile
        entity.save()

        skills_data = self.initial_data.get('skills', None)
        if skills_data:
            skills_data = [dict(skill, profile=entity.pk) for skill in skills_data]
            userskill_serializer = UserSkillSerializer(data=skills_data, many=True)
            userskill_serializer.is_valid(raise_exception=True)
            userskill_serializer.save()
        return entity

    def update(self, instance, validated_data):
        validated_data.pop("skills", None)
        instance = Entity(pk=instance.pk, **validated_data)

        skills_data = self.initial_data.get('skills', None)
        if skills_data:
            instance.skills.clear()
            skills_data = [dict(skill, profile=instance.pk) for skill in skills_data]
            userskill_serializer = UserSkillSerializer(data=skills_data, many=True)
            userskill_serializer.is_valid(raise_exception=True)
            userskill_serializer.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    links = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('user', 'is_employer', 'links')

    def get_links(self, obj):
        request = self.context['request']
        entity_relative_url = reverse('api:entity-list',
                                      kwargs={
                                          'parent_lookup_profile': obj.user.username
                                      })
        entity_absolute_url = request.build_absolute_uri(entity_relative_url)
        self_relative_url = reverse('api:user-profile-detail',
                                    kwargs={
                                        'user__username': obj.user.username
                                    })
        self_absolute_url = request.build_absolute_uri(self_relative_url)
        return {
            'entities': entity_absolute_url,
            'self': self_absolute_url,
        }
