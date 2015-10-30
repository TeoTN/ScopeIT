# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from api.profile.views import ProfileViewSet, SkillsViewSet
from rest_framework.routers import DefaultRouter
from django.conf.urls import include, url


router = DefaultRouter()
router.register('users', ProfileViewSet, base_name='user')
router.register('skills', SkillsViewSet, base_name='skill')
urlpatterns = [
    url(r'', include(router.urls)),
]
