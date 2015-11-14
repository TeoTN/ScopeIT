# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib import admin

from common.views import IndexView
from accounts.views import GoogleLogin
import accounts.urls

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(accounts.urls)),
    url(r'^api/v1/', include("api.urls", namespace='api')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/google/$', GoogleLogin.as_view(), name='google_login')
]
