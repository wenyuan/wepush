# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import requests
from django.conf import settings

from project_apps.users.models import Manager
from project_apps.wechat.models import AccessToken, ScanEvent

WECHAT_APPID = settings.WECHAT_APPID
WECHAT_APPSECRET = settings.WECHAT_APPSECRET


def bound_handle(openid, eventkey):
    try:
        managers = Manager.objects.filter(openids__contains=openid)
        if managers:
            content = ('您已经绑定过' + managers[0].username).encode('utf-8')
        else:
            scan_events = ScanEvent.objects.filter(eventkey=eventkey)
            if scan_events:
                scan_event = scan_events[0]
                manager = scan_event.manager
                username = manager.username
                openids = manager.openids
                if not openids:
                    manager.openids = json.dumps([openid])
                    manager.save()
                else:
                    openid_list = json.loads(openids)
                    openid_list.append(openid)
                    openids = json.dumps(openid_list)
                    manager.openids = openids
                    manager.save()
                content = ('恭喜您绑定成功' + username).encode('utf-8')
            else:
                content = '请刷新重试'
        return content
    except Exception, e:
        print(e)


def unbound_handle(openid):
    managers = Manager.objects.filter(openids__contains=openid)
    for manager in managers:
        openids = manager.openids
        openid_list = json.loads(openids)
        openid_list.remove(openid)
        openids = json.dumps(openid_list)
        manager.openids = openids
        manager.save()


def get_qrcode_ticket(expire_seconds, scene_id):
    # 获取access_token（公众号调用各接口时都需使用access_token）
    access_token = get_access_token()
    url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={access_token}'.format(
        access_token=access_token
    )
    body = dict(
        expire_seconds=expire_seconds,
        action_name='QR_STR_SCENE',
        action_info=dict(
            scene=dict(
                scene_str=scene_id
            )
        )
    )
    # FIXME...微信要传字符串格式的body，不然会报错（invalid action name）
    body = json.dumps(body)
    res = requests.post(url, data=body)
    return json.loads(res.text)


def get_access_token():
    access_tokens = AccessToken.objects.all()
    if not access_tokens:
        # 从远端获取access_token
        res = real_get_access_token()
        AccessToken.objects.create(access_token=res['access_token'], expires_in=res['expires_in'])
        return res['access_token']
    else:
        # 从本地获取access_token
        access_token = access_tokens[0]
        return access_token.access_token


def real_get_access_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}'.format(
        appid=WECHAT_APPID,
        secret=WECHAT_APPSECRET
    )
    res = requests.get(url)
    return json.loads(res.text)


def send_template_message(data_tuple):
    access_token = get_access_token()
    print('=====')
    print(access_token)
    print('====')
    post_url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}'.format(
        access_token=access_token)
    post_data = TEST_TPL % data_tuple
    res = requests.post(post_url, data=post_data)
    return json.loads(res.text)


""" 模板内容
{{first.DATA}}
时间：{{keyword1.DATA}}
内容：{{keyword2.DATA}}
建议：{{keyword3.DATA}}
{{remark.DATA}}
"""
TEST_TPL = """
{
    "touser": "%s",
    "template_id": "%s",
    "url": "%s",
    "miniprogram": {
        "appid": "",
        "pagepath": ""
    },
    "data": {
        "first": {
            "value": "%s",
            "color": "#173177"
        },
        "keyword1": {
            "value": "%s",
            "color": "#173177"
        },
        "keyword2": {
            "value": "%s",
            "color": "#173177"
        },
        "keyword3": {
            "value": "%s",
            "color": "#173177"
        },
        "remark": {
            "value": "%s",
            "color": "#173177"
        }
    }
}
"""
