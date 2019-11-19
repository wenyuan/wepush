# -*- coding: utf-8 -*-

""" 模板内容
{{first.DATA}}
时间：{{keyword1.DATA}}
内容：{{keyword2.DATA}}
建议：{{keyword3.DATA}}
{{remark.DATA}}
"""
TEST_TPL = """
{
    "touser": "{openid}",
    "template_id": "{template_id}",
    "url": "{url}",
    "miniprogram": {
        "appid": "",
        "pagepath": ""
    },
    "data": {
        "first": {
            "value": "{first}",
            "color": "#173177"
        },
        "keyword1": {
            "value": "{keyword1}",
            "color": "#173177"
        },
        "keyword2": {
            "value": "{keyword2}",
            "color": "#173177"
        },
        "keyword3": {
            "value": "{keyword3}",
            "color": "#173177"
        },
        "remark": {
            "value": "{remark}",
            "color": "#173177"
        }
    }
}
"""
