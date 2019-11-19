# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views
from . import apis

app_name = 'wechat'

urlpatterns = [
    url(r'^$', apis.index, name='wechat_index'),
    url(r'^get_qrcode/$', apis.get_qrcode, name='wechat_get_qrcode'),
    url(r'^refresh_qrcode/$', apis.refresh_qrcode, name='wechat_refresh_qrcode'),
]
