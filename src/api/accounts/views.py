from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework_extensions.mixins import NestedViewSetMixin

from .serializers import (
    SkillSerializer,
    UserSkillSerializer,
    UserProfileSerializer,
    EntitySerializer,
    MatchesSerializer
)

from accounts.models import (
    Skill,
    UserSkill,
    UserProfile,
    Entity,
)
from api.permissions import UserProfilePermission, EntityPermission


class UserProfileViewSet(NestedViewSetMixin, ModelViewSet):
    """
    This view presents a user's profile. Each profile provides an additional link to *entities*
    related to the profile.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user__username'
    lookup_value_regex = '[0-9a-zA-Z]+'
    permission_classes = (IsAuthenticated, UserProfilePermission,)


class SkillsViewSet(NestedViewSetMixin, ModelViewSet):
    """
    This endpoint lists all skills available.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class EntityViewSet(NestedViewSetMixin, ModelViewSet):
    """
    Within this view all entities belonging to a given user are displayed. The entity is a set of requirements and
     offerings which can be interpreted either as a job ad (posted by employer) or as a applicant characteristics.
    """
    serializer_class = EntitySerializer
    permission_classes = (IsAuthenticated, EntityPermission)

    def get_queryset(self):
        return Entity.objects.filter(user_profile__user__username=self.kwargs['parent_lookup_profile'])


class MatchesViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = MatchesSerializer

    def get_queryset(self):
        entity_id = self.kwargs['parent_lookup_entity']
        mine = Entity.objects.filter(pk=entity_id)
        theirs = Entity.objects.filter(match__pk=entity_id)
        return mine | theirs


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
