# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
import datetime
import random
import json
import hashlib
import requests
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
from django.conf import settings

from project_apps.wechat.models import ScanEvent
from project_apps.users.models import Manager
from .utils import bound_handle, unbound_handle, get_qrcode_ticket, send_template_message
from .cron import refresh_access_token
import receive
import reply

WECHAT_TOKEN = settings.WECHAT_TOKEN


@csrf_exempt
def index(request):
    if request.method == 'GET':
        try:
            signature = request.GET.get('signature', None)
            timestamp = request.GET.get('timestamp', None)
            nonce = request.GET.get('nonce', None)
            echostr = request.GET.get('echostr', None)
            param_list = [WECHAT_TOKEN, timestamp, nonce]
            param_list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, param_list)
            hashcode = sha1.hexdigest()
            if hashcode == signature:
                return HttpResponse(echostr)
            else:
                return HttpResponse('')
        except Exception, Argument:
            return HttpResponseBadRequest(Argument)
    if request.method == 'POST':
        try:
            xml_str = smart_str(request.body)
            recMsg = receive.parse_xml(xml_str)
            if isinstance(recMsg, receive.EventMsg):
                user_openid = recMsg.FromUserName
                developer_wxid = recMsg.ToUserName
                if recMsg.Event == 'SCAN':
                    if recMsg.EventKey:
                        content = bound_handle(user_openid, recMsg.EventKey)
                        replyMsg = reply.TextMsg(user_openid, developer_wxid, content)
                        return HttpResponse(replyMsg.send())
                if recMsg.Event == 'subscribe':
                    if recMsg.EventKey and recMsg.EventKey.startswith('qrscene_'):
                        content = bound_handle(user_openid, recMsg.EventKey[8:])
                        replyMsg = reply.TextMsg(user_openid, developer_wxid, content)
                        return HttpResponse(replyMsg.send())
                if recMsg.Event == 'unsubscribe':
                    unbound_handle(user_openid)
            return HttpResponse(reply.Msg().send())
        except Exception, Argument:
            return HttpResponseBadRequest(Argument)


@login_required
def get_qrcode(request):
    if request.method == 'GET':
        manager = request.user
        try:
            scan_event = manager.scan_event
            ticket = scan_event.ticket
            imgurl = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={ticket}'.format(ticket=ticket)
            if requests.get(imgurl).status_code == 200:
                return JsonResponse({
                    'code': 200,
                    'result': 'success',
                    'msg': _('QR code.二维码。'),
                    'data': dict(
                        manager=manager.username,
                        qrcode=imgurl
                    )
                })
            else:
                return JsonResponse({
                    'code': 404,
                    'result': 'failure',
                    'msg': _('二维码已过期，请刷新二维码'),
                    'data': dict(
                        manager=manager.username,
                        qrcode=imgurl
                    )
                })
        except ScanEvent.DoesNotExist:
            return JsonResponse({
                'code': 400,
                'result': 'failure',
                'msg': _('获取二维码失败，请刷新二维码'),
                'data': dict(
                    manager=manager.username,
                    qrcode=''
                )
            })
    elif request.method == 'POST':
        return HttpResponseNotAllowed(['GET'])


@login_required
def refresh_qrcode(request):
    if request.method == 'POST':
        manager = request.user
        params = json.loads(request.body)
        expire_seconds = params.get('expire_seconds', 60 * 60 * 24 * 7)

        expired_time = datetime.datetime.now() + datetime.timedelta(seconds=expire_seconds)
        scene_id = str(int(time.time() * 1000)) + str(random.randint(0, 10000))
        # 向微信开发者平台请求二维码ticket，凭借此ticket可以在有效时间内换取二维码
        result = get_qrcode_ticket(expire_seconds, scene_id)
        # 通过ticket换取二维码
        ticket = result.get('ticket')
        if not ticket:
            return HttpResponseBadRequest(json.dumps(result), content_type='application/json')
        try:
            scan_event = manager.scan_event
            scan_event.eventkey = scene_id
            scan_event.ticket = ticket
            scan_event.expired_time = expired_time
            scan_event.save()
        except ScanEvent.DoesNotExist:
            ScanEvent.objects.create(manager=manager, eventkey=scene_id, ticket=ticket, expired_time=expired_time)
        imgurl = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={ticket}'.format(ticket=ticket)
        return JsonResponse({
            'code': 200,
            'result': 'success',
            'msg': _('QR code.二维码。'),
            'data': dict(
                manager=manager.username,
                qrcode=imgurl
            )
        })
    elif request.method == 'GET':
        return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def send_message(request, manager_guid):
    if request.method == 'POST':
        params = json.loads(request.body)
        # 模板消息内容
        # TODO...此处是测试账号的模板消息内容
        url = params.get('url', '')
        first = params.get('url', '')
        keyword1 = params.get('keyword1', '')
        keyword2 = params.get('keyword2', '')
        keyword3 = params.get('keyword3', '')
        remark = params.get('remark', '')

        try:
            manager = Manager.objects.get(guid=manager_guid)
            if not manager.is_active:
                return JsonResponse({
                    'code': 400,
                    'result': 'failure',
                    'msg': _('This manager has not been confirmed.没有激活'),
                    'data': {}
                })
            # 推送消息
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            current_timestamp = int(time.time())
            call_interval = manager.call_interval
            last_call_timestamp = time.mktime(manager.last_call.timetuple())
            delta_timestamp = current_timestamp - last_call_timestamp
            if delta_timestamp < call_interval:
                msg = _('请在{delta_timestamp}s后再次推送（当前限制推送间隔为{call_interval}s/次）.'.format(delta_timestamp=60-delta_timestamp, call_interval=call_interval))
                return JsonResponse({
                    'code': 400,
                    'result': 'failure',
                    'msg': msg,
                    'data': {}
                })

            username = manager.username
            openids = manager.openids
            openid_list = json.loads(openids)
            result_list = []
            if not openid_list:
                msg = _('没有用户要推送.')
                return JsonResponse({
                    'code': 400,
                    'result': 'failure',
                    'msg': msg,
                    'data': {}
                })
            for openid in openid_list:
                # TODO...此处是测试账号的template_id
                template_id = 'SXadYf6tGXHLg-VtYVY6L-o58C_qUlX853iRl3_3zWc'
                keyword1 = current_time
                data_tuple = (openid, template_id, url, first, keyword1, keyword2, keyword3, remark)
                result = send_template_message(data_tuple)
                result_list.append({'openid': openid, 'result': result})
            manager.last_call = current_time
            manager.save()
            return JsonResponse({
                'code': 200,
                'result': 'success',
                'msg': _('Send template message successfully.'),
                'data': result_list
            })
        except Manager.DoesNotExist:
            msg = _('你无权推送.')
        except Exception as e:
            print(e)
            msg = _('Something wrong when send template message.有异常')
        return JsonResponse({
            'code': 400,
            'result': 'failure',
            'msg': msg,
            'data': {}
        })
    elif request.method == 'GET':
        return HttpResponseNotAllowed(['POST'])


@login_required
def refresh_token(request):
    if request.method == 'POST':
        try:
            refresh_access_token()
            return JsonResponse({
                'code': 200,
                'result': 'success',
                'msg': _('刷新access token成功'),
                'data': {}
            })
        except Exception, Argument:
            return HttpResponseBadRequest(Argument)
    elif request.method == 'GET':
        return HttpResponseNotAllowed(['POST'])
