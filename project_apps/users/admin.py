# -*- coding: utf-8 -*-
# https://www.cnblogs.com/caseast/p/5909987.html
# https://www.cnblogs.com/wumingxiaoyao/p/6928297.html
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Manager


class SiteUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'description', 'openids', 'is_active', 'is_staff', 'is_superuser',)
    list_filter = ('is_active', 'is_staff', 'is_superuser',)
    search_fields = ('username', 'org_name',)
    ordering = ('id',)
    fieldsets = (
        ('Account info', {'fields': ('username', 'password', 'email', 'created_time', 'updated_time')}),
        ('Wechat info', {'fields': ('guid', 'description', 'openids', 'call_interval', 'last_call')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
    )
    readonly_fields = ('created_time', 'updated_time')


admin.site.register(Manager, SiteUserAdmin)
admin.site.unregister(Group)

admin.site.site_header = 'WePush后台管理'
admin.site.site_title = 'WePush后台管理'
