# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.views.generic import TemplateView
from accounts.views import (
    ProfileView,
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

    url(r'^matches/',
        TemplateView.as_view(template_name='account/matches.html'),
        name='matches'),
]
