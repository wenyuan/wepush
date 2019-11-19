# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser

from generic.forms.fields import GUIDField


class Manager(AbstractUser, models.Model):
    id = models.AutoField(primary_key=True)
    guid = GUIDField(_('guid'), unique=True)
    username = models.CharField(max_length=128, unique=True, verbose_name=_('username'))
    password = models.CharField(max_length=256, verbose_name=_('password'))
    email = models.EmailField(verbose_name=_('email'))
    description = models.CharField(max_length=128, default='chaincloud', verbose_name=_('description'))
    openids = models.TextField(default='[]', verbose_name=_('openids'))
    call_interval = models.PositiveIntegerField(default=60, verbose_name=_('call interval(seconds)'))
    last_call = models.DateTimeField(default=datetime.datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
                                     verbose_name=_('last call'))
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('created time'))
    updated_time = models.DateTimeField(auto_now=True, verbose_name=_('updated time'))
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'manager'
        verbose_name = _('manager')
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
