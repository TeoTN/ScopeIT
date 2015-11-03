# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

#from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedDefaultRouter

from api.profile.views import UserProfileViewSet, ProfessionalProfileViewSet


router = ExtendedDefaultRouter()

profile_routes = router.register('profiles',
                                      UserProfileViewSet,
                                      base_name='user-profile')

profile_routes.register('professional',
                        ProfessionalProfileViewSet,
                        base_name='professional-profile',
                        parents_query_lookups=['profile'])

urlpatterns = [
    url(r'', include(router.urls)),
]
