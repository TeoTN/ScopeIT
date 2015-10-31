from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .serializers import UserSerializer, SkillSerializer
from app_profile.models import Profile, Skill
from api.permissions import IsObjectOwnerOrAdmin, IsAdminOrReadOnly


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsObjectOwnerOrAdmin, IsAdminOrReadOnly)


class SkillsViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
