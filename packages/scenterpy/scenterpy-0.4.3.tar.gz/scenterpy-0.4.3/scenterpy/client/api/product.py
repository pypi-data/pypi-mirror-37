# -*- coding: utf-8 -*-

from .base import BaseSCenterAPI

class Product(BaseSCenterAPI):
    path = 'ec_products/'

    def get(self, slug=None):
        """
        查询商品信息
        :param slug:
        :return:
        """
        return self._get('{}{}/'.format(self.path, slug)).json()

    def list(self):
        """
        获取商品列表
        :param slug:
        :return:
        """
        return self._get(self.path).json()
