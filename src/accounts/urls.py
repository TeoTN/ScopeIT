# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from accounts.views import (
    ProfileView,
    EntityFormView,
)

urlpatterns = [
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'}),

    url(r'^',
        include('allauth.urls')),

    url(r'^profile/',
        ProfileView.as_view(),
        name='profile'),

    url(r'^entity-form/$',
        EntityFormView.as_view(),
        name='entity-form'),
]
