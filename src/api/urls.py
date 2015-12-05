# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from rest_framework_extensions.routers import ExtendedDefaultRouter

from api.accounts.views import (
    UserProfileViewSet,
    EntityViewSet,
    SkillsViewSet,
    MatchesViewSet
)
from accounts.views import GoogleLogin

router = ExtendedDefaultRouter()

profile_routes = router.register('profiles',
                                 UserProfileViewSet,
                                 base_name='user-profile')

entity = profile_routes.register('entity',
                        EntityViewSet,
                        base_name='entity',
                        parents_query_lookups=['profile'])

entity.register('matches',
                MatchesViewSet,
                base_name='matches',
                parents_query_lookups=['profile', 'entity'])

router.register('skills',
                SkillsViewSet,
                base_name='skill')

urlpatterns = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/google/$', GoogleLogin.as_view(), name='google_login')
]+router.urls
