# -*- coding: utf-8 -*-

import json

from .base import BaseSCenterAPI


class Common(BaseSCenterAPI):
    def signing(self, signing_dict):
        """
        签名
        :param order_dict: 格式参考
        :return:
        """
        return self._post('common/signing/', json=signing_dict).json()

    def odoo_docking(self, data):
        """
        内部商城odoo实例对接平台接口
        :param data:
        :return:
        """
        return self._post('common/docking/', json=data).json()
