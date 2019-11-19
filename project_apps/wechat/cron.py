# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
import datetime
import random
from apscheduler.scheduler import Scheduler

from .models import AccessToken, ScanEvent
from .utils import real_get_access_token, get_qrcode_ticket


def refresh_access_token():
    """
    access_token的有效期目前为2个小时，需定时刷新
    :return:
    """
    res = real_get_access_token()
    access_tokens = AccessToken.objects.all()
    if not access_tokens:
        # 从远端获取access_token
        AccessToken.objects.create(access_token=res['access_token'], expires_in=res['expires_in'])
    else:
        # 更新本地access_token
        access_token = access_tokens[0]
        access_token.access_token = res['access_token']
        access_token.expires_in = res['expires_in']
        access_token.save()


def refresh_scan_event():
    """
    刷新Eventkey中的scene_id，从而刷新临时二维码
    临时二维码有效期默认7天
    在过期前1小时就自动进行刷新
    :return:
    """
    scan_events = ScanEvent.objects.all()
    for scan_event in scan_events:
        username = scan_event.manager.username
        expired_time = scan_event.expired_time
        if time.mktime(expired_time.timetuple()) - time.time() < 60 * 60 * 1:
            print('{username}的ticket过期了'.format(username=username))
            scene_id = str(int(time.time() * 1000)) + str(random.randint(0, 10000))
            expire_seconds = 60 * 60 * 24 * 7
            expired_time = datetime.datetime.now() + datetime.timedelta(seconds=expire_seconds)
            result = get_qrcode_ticket(expire_seconds, scene_id)
            # 通过ticket换取二维码
            ticket = result.get('ticket')
            scan_event.eventkey = scene_id
            scan_event.ticket = ticket
            scan_event.expired_time = expired_time
            scan_event.save()
        else:
            print('{username}的ticket没有过期'.format(username=username))


sched = Scheduler()


@sched.interval_schedule(hours=1, minutes=50)
def cron_task1():
    print('定时任务1开始\n')
    refresh_access_token()
    print('定时任务1结束\n')


@sched.interval_schedule(hours=1)
def cron_task2():
    print('定时任务2开始\n')
    refresh_scan_event()
    print('定时任务2结束\n')


sched.start()
