from django.contrib.auth.models import User

from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from app_profile.models import Profile, Skill


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill


class ProfileSerializer(ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = Profile
        fields = ('skills',)


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    links = SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'profile', 'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('api:user-detail',
                kwargs={'pk': obj.pk},
                request=request),
        }
