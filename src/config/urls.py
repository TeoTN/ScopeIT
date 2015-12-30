# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib import admin

from common.views import IndexView
import accounts.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(accounts.urls)),
    url(r'^api/v1/', include("api.urls", namespace='api')),
    url('^.*$', IndexView.as_view(), name='index'),
]


