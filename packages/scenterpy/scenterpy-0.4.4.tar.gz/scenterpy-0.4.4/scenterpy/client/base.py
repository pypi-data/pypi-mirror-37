# -*- coding: utf-8 -*-

import datetime

import requests

try:
    from urllib.parse import urljoin
except:
    from urllib.parse import urljoin


class BaseSCenterClient(object):
    requests = requests.Session()
    base_url = 'http://supplier.cognichain.com/'

    def __init__(self, username=None, password=None, base_url=base_url, token=None, expires=None, session=None,
                 retry_time=3):
        self.retry_time = retry_time
        self.auth_ok = False
        self.username = username
        self.password = password
        self.base_url = base_url
        self.expires = expires
        self.api_base_url = urljoin(base_url, 'api/v2/')

        if token:
            self.token = token
            self.requests.headers.update({
                'Authorization': 'JWT {}'.format(token)
            })
        else:
            self.fetch_token(username, password)

    def fetch_token(self, username, password):
        """
        请求获取token（没有token或token失效都调用这里）
        :param username:
        :param password:
        :return:
        """
        url = urljoin(self.base_url, 'api-token-auth/')
        r = self.requests.post(url, json={'username': username, 'password': password})
        self.token = r.json().get('token')
        expires = r.json().get('expires')
        if expires:
            self.expires = datetime.datetime.strptime(expires, "%Y-%m-%dT%H:%M:%S.%f")
        self.requests.headers.update({
            'Authorization': 'JWT {}'.format(self.token)
        })
        self.auth_ok = True
        return self.token

    def refresh_token(self):
        """
        此接口用于在token未设置过期时间的情况下使用，传递的token必须是有效的。
        :return:
        """
        url = urljoin(self.base_url, 'api-token-refresh/')
        r = self.requests.post(url, json={'token': self.token})
        self.token = r.json().get('token')
        self.requests.headers.update({
            'Authorization': 'JWT {}'.format(self.token)
        })
        return self.token

    def get(self, url, **kwargs):
        return self.handle_response(method='get', url=url, **kwargs)

    def post(self, url, **kwargs):
        return self.handle_response(method='post', url=url, **kwargs)

    def patch(self, url, **kwargs):
        return self.handle_response(method='patch', url=url, **kwargs)

    def handle_response(self, method, url, **kwargs):
        r = None
        if method == 'get':
            r = self.requests.get(urljoin(self.api_base_url, url), **kwargs)
        elif method == 'patch':
            r = self.requests.patch(urljoin(self.api_base_url, url), **kwargs)
        elif method == 'post':
            r = self.requests.post(urljoin(self.api_base_url, url), **kwargs)

        status_code = r.status_code
        if status_code >= 400 and status_code != 404:
            if status_code == 511:
                self.auth_ok = False
                raise ValueError('平台认证出错误，请联系管理员')

            # todo 状态码统一处理
            token_error = r.json().get("detail", None)
            if token_error:
                self.fetch_token(self.username, self.password)
                r = self.requests.post(urljoin(self.api_base_url, url), **kwargs)

        elif status_code == 404:
            raise LookupError('未找该资源')
        return r
