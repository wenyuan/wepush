# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render


@login_required
def index(request):
    context = dict(
        current_time=datetime.datetime.now().strftime('%Y-%m-%d'),
    )

    return render(request, 'index.html', context=context)


@login_required
def debugger(request):
    context = dict(
        current_time=datetime.datetime.now().strftime('%Y-%m-%d'),
    )

    return render(request, 'debugger.html', context=context)
