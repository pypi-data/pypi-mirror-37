# coding:UTF-8


"""
基于HTTP2的苹果推送 增加证书验证参数cert_password
@author: geyouwen
创建于2016年11月18日
"""

from hyper import HTTPConnection, tls
import re
import json


class AppleHttp2Push:
    def __init__(self, cert, apns_topic, cert_password, is_production_server = False):
        self.cert = cert
        self.cert_password = cert_password
        self.headers = {"apns-topic": apns_topic}
        self.api_url = 'api.push.apple.com:443' if is_production_server else 'api.development.push.apple.com:443'
        self.api_path = '/3/device/%s'

    def get_api_path(self, token):
        """
        获取请求的API路径
        :param token:
        :return:
        """
        return self.api_path % token

    @staticmethod
    def make_response(r):
        """
        封装返回对象
        :param r:
        :return:
        """
        data = r.read()
        try:
            data = json.loads(data)
        except ValueError:
            data = {}
        status = r.status

        return {
            "data": data,
            "status": status,
            "error_msg": data.get('reason', '未知错误') if data else None,
            "headers": dict(r.headers)
        }

    @staticmethod
    def handle_token(token):
        """
        处理token
        :param token: 苹果设备token
        :return:
        """
        if re.match(r'<.*?>', token):
            token = token[1:-1]
        return token.replace(" ", '')

    def push(self, token, alert_title='', alert_body='', badge=1, sound='default'):
        """
            发送单个设备
            :param token:设备
            :param alert_title:弹出的消息title加粗
            :param alert_body:弹出的消息title加粗
            :param badge:红点数字
            :param sound:声音
            :return:
            """
        token = self.handle_token(token)
        payload = {
            'aps': {
                'alert': alert_title,
                'body': alert_body,
                'content-available':1,
                'sound': sound,
                'badge': badge,

            }
        }
        conn = HTTPConnection(self.api_url, ssl_context=tls.init_context(cert=self.cert, cert_password=self.cert_password))
        conn.request('POST', self.get_api_path(token), body=json.dumps(payload), headers=self.headers)
        resp = conn.get_response()
        return self.make_response(resp)

    @staticmethod
    def doc():
        print("具体请参考：https://developer.apple.com/library/prerelease/content/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/CommunicatingwithAPNs.html#//apple_ref/doc/uid/TP40008194-CH11-SW1")

