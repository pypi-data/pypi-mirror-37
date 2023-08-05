# -*- coding: utf-8 -*-

from .base import BaseSCenterAPI


class Partner(BaseSCenterAPI):
    path = 'ec_partners/'

    def msg(self, data):
        """
        :param data:
        {
            user_slugs:['123as231','ae563ef']
            msg: {
                'title':'消息标题',
                'description':'消息描述',
                'url':'跳转链接',
            }
        }
        :return:
        """
        path = self.path + 'msg/'
        return self._post(path, json=data).json()

    def tag(self, data):
        path = self.path + 'tag/'
        return self._post(path, json=data).json()

    def get(self, slug=None):
        """
        :param slug:
        :return:
        """
        return self._get('{}{}/'.format(self.path, slug)).json()

    def list(self, page=1, name=None):
        """
        :param page: 页码
        :param name: 供应商名称
        :return:
        """
        params = {'page': page}
        if name:
            params.update({'name': name})
        return self._get(self.path, params=params).json()

        # def search(self, q_name):
        #     """
        #     按名称模糊搜索供应商
        #     :param q_name:
        #     :return:
        #     [
        #         {
        #         "id": 98,
        #         "name": "saas商城邀请的第一个供应商",
        #         "slug": "a5b675ec",
        #         "desc": null
        #         },
        #         {
        #         "id": 97,
        #         "name": "saas对接测试",
        #         "slug": "f605181d",
        #         "desc": "saas对接测试"
        #         }
        #     ]
        #     """
        #     return self.list(params={'q': q_name}).get('results', [])
        #

    def config(self,data):
        path = self.path + 'config/'
        return self._post(path, json=data).json()

