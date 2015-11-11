# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework_extensions.routers import ExtendedDefaultRouter

from api.accounts.views import UserProfileViewSet, EntityViewSet, SkillsViewSet


router = ExtendedDefaultRouter()

profile_routes = router.register('profiles',
                                 UserProfileViewSet,
                                 base_name='user-profile')

profile_routes.register('entity',
                        EntityViewSet,
                        base_name='entity',
                        parents_query_lookups=['profile'])

router.register('skills',
                SkillsViewSet,
                base_name='skill')

urlpatterns = router.urls
