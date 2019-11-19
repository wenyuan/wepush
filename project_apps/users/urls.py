# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views, apis

app_name = 'users'

urlpatterns = [
    url(r'^login\.html$', TemplateView.as_view(template_name='login.html'), name='user_login'),

    url(r'^login/$', apis.on_user_login),
    url(r'^logout/$', apis.on_user_logout),
]
