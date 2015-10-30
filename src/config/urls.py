# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from app_profile.views import ProfileView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', ProfileView.as_view()),
    url(r'^api/', include("api.urls", namespace='api')),
]

