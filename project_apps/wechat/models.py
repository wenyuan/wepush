# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser

from generic.forms.fields import GUIDField
from project_apps.users.models import Manager


class AccessToken(models.Model):
    id = models.AutoField(primary_key=True)
    access_token = models.CharField(max_length=256, verbose_name=_('access_token'))
    expires_in = models.IntegerField(verbose_name=_('expires_in'))
    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('created time'))
    updated_time = models.DateTimeField(auto_now=True, null=True, verbose_name=_('updated time'))

    def __str__(self):
        return 'AccessToken'

    class Meta:
        db_table = 'access_token'
        verbose_name = _('access token')
        verbose_name_plural = verbose_name
        ordering = ['-created_time']


class ScanEvent(models.Model):
    id = models.AutoField(primary_key=True)
    manager = models.OneToOneField(Manager, on_delete=models.CASCADE, related_name='scan_event', verbose_name=_('related manager'))
    eventkey = models.CharField(max_length=64, verbose_name=_('eventkey(scene_id)'))
    ticket = models.CharField(max_length=256, verbose_name=_('ticket'))
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('created time'))
    updated_time = models.DateTimeField(auto_now=True, verbose_name=_('updated time'))
    expired_time = models.DateTimeField(verbose_name=_('expired time'))

    def __str__(self):
        return 'ScanEvent - {username}({description})'.format(username=self.manager.username, description=self.manager.description)

    class Meta:
        db_table = 'scan_event'
        verbose_name = _('scan event')
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
