# -*- coding: utf-8 -*-

import json


class BaseSCenterAPI(object):
    def __init__(self, client=None):
        self._client = client

    def _get(self, url, **kwargs):
        return self._client.get(url, **kwargs)

    def _post(self, url, **kwargs):
        return self._client.post(url, **kwargs)

    def _patch(self, url, **kwargs):
        return self._client.patch(url, **kwargs)


class BaseModelAPI(BaseSCenterAPI):
    """
    CURD基本操作的model配置path即可
    有特殊接口的model，继承本类
    """

    def __init__(self, client, path=None):
        super(BaseModelAPI, self).__init__(client)
        if path:
            self.path = path
            if not path.endswith('/'):
                self.path = path + '/'

    def create(self, data):
        """
        :param data:
        :return:
        """
        return self._post(self.path, json=data).json()

    def get(self, slug=None):
        """
        :param slug:
        :return:
        """
        return self._get("{}{}/".format(self.path, slug)).json()

    def list(self, **kwargs):
        """
        :param slug:
        :return:
        """
        return self._get(self.path, **kwargs).json()

    def update(self, slug, data):
        return self._patch("{}{}/".format(self.path, slug), json=data).json()
