#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

# 企业ID（用户提供）
corpid = 'ww77sw181b21aaac08'
# 应用Secret（用户创建应用并提供）
corpsecret = 'Pmnu9dwedOgHtAfEZBydefDTm6J6AdsqwqqxDt_r-jM'
# 应用AgentId
agentid = 1000009
# 部门ID列表（企业id/部门id）
partyid = 2


def get_token():
    """
    根据API获取token
    corpid: 获取到的企业ID
    corpsecret：应用的secret
    """
    req_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    req_params = {
        'corpid': corpid,
        'corpsecret': corpsecret,
    }
    res = requests.post(req_url, params=req_params)
    data = json.loads(res.text)
    return data["access_token"]


def send_msg(content):
    """
    调用企业微信发送信息API
    参考链接 https://work.weixin.qq.com/api/doc#10167
    """
    req_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}".format(
        access_token=get_token()
    )
    req_body = {
        "toparty": partyid,
        "msgtype": "textcard",
        "toall": 0,
        "agentid": agentid,
        "textcard": content,
        "safe": 0
    }
    try:
        res = requests.post(req_url, json.dumps(req_body, ensure_ascii=False))
        result = json.loads(res.content.decode())
        if result["errmsg"] != "ok":
            print(result)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    import datetime

    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    description = """
    <div class="gray">{current_time}</div>
    <div class="normal">这是一条</div>
    <div class="highlight">请于今晚18:00后领取</div>
    """.format(current_time=current_time)
    content = dict(
        title='提醒加班小助手',
        description=description,
        url='https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1573471877461&di=79bffa739faed39d1895466b56446d39&imgtype=0&src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fitem%2F201608%2F09%2F20160809175554_Z2kwB.thumb.700_0.gif',
        btntxt='更多'
    )

    send_msg(content)
