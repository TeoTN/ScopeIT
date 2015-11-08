from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework_extensions.mixins import DetailSerializerMixin, NestedViewSetMixin

from .serializers import (
    SkillSerializer,
    UserSkillSerializer,
    UserProfileSerializer,
    EntitySerializer
)
from accounts.models import Skill, UserSkill, UserProfile, Entity


class UserProfileViewSet(NestedViewSetMixin, ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user__username'
    lookup_value_regex = '[0-9a-zA-Z]+'


class SkillsViewSet(NestedViewSetMixin, ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class UserProfileView(ModelViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class EntityViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = EntitySerializer

    def get_queryset(self):
        return Entity.objects.filter(user_profile__user=self.request.user)


class UserSkillsView(ListModelMixin,
                     CreateModelMixin,
                     GenericAPIView):
    """
        This view is used to list and create skills of a user
    """

    serializer_class = UserSkillSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return UserSkill.objects.filter(profile__user=user)
