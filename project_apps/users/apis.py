# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.utils import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password

from .models import Manager


def on_user_login(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        auth.logout(request)
        username = params.get('username', '')
        password = params.get('password', '')
        redirect_url = params.get('next', '')
        if not username or not password:
            return JsonResponse({
                'code': 400,
                'result': 'failure',
                'msg': _('Username/password should not be empty.'),
                'data': {}
            })
        try:
            manager = Manager.objects.get(username=username)
            if not manager.is_active:
                return JsonResponse({
                    'code': 400,
                    'result': 'failure',
                    'msg': _('This user has not been confirmed.'),
                    'data': {}
                })
            if check_password(password, manager.password):
                auth.login(request, manager)
                return JsonResponse({
                    'code': 200,
                    'result': 'success',
                    'msg': _('Login successfully.'),
                    'data': dict(
                        redirect_url=redirect_url if redirect_url else settings.LOGIN_REDIRECT_URL
                    )
                })
            else:
                msg = _('Username/password incorrect.')
        except Manager.DoesNotExist:
            msg = _('Username/password incorrect.')
        except Exception as e:
            msg = _('Something wrong when ask for login.')

        return JsonResponse({
            'code': 400,
            'result': 'failure',
            'msg': msg,
            'data': {}
        })
    elif request.method == 'GET':
        return HttpResponseNotAllowed(['POST'])


def on_user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
