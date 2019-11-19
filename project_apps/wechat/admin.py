# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import AccessToken, ScanEvent


class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_time', 'updated_time', 'expires_in',)
    ordering = ('id',)
    readonly_fields = ('access_token', 'expires_in', 'created_time', 'updated_time')


class ScanEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'manager', 'eventkey', 'created_time', 'updated_time', 'expired_time',)
    ordering = ('id',)
    readonly_fields = ('eventkey', 'ticket', 'created_time', 'updated_time', 'expired_time')


admin.site.register(AccessToken, AccessTokenAdmin)
admin.site.register(ScanEvent, ScanEventAdmin)
