# -*- coding: utf-8 -*-
import os
import sys
import django
from functools import reduce

reload(sys)
sys.setdefaultencoding('utf-8')

BASE_DIR = reduce(lambda x, y: os.path.dirname(x), range(2), os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'wepush.settings'
django.setup()

from django.db.models import Q
from django.contrib.auth import get_user_model


def auto_create_superuser():
    username = 'admin'
    email = 'wenyuan.xu@vip.163.com'
    password = 'password'

    UserModel = get_user_model()
    if not UserModel.objects.filter(Q(username=username) | Q(email=email)):
        print('Creating superuser ({0}:{1}:{2})'.format(username, email, password))
        user = UserModel.objects.create_superuser(username, email, password)
        user.nickname = username
        user.is_active = True
        user.save()
    else:
        print('Superuser already existed.')


if __name__ == "__main__":
    auto_create_superuser()
