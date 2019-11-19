"""wepush URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

from project_apps.users import views as user_views
from project_apps.wechat import apis as wechat_apis
import project_apps.wechat.cron

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', user_views.index),
    url(r'^index(?:\.html|php)?$', user_views.index),
    url(r'^debugger(?:\.html|php)?$', user_views.debugger),
    url(r'^users/', include('project_apps.users.urls')),
    url(r'^wx/', include('project_apps.wechat.urls')),
    url(r'^(?P<manager_guid>\w+)\.send$', wechat_apis.send_message),
    url(r'^refresh_token/$', wechat_apis.refresh_token),
]
