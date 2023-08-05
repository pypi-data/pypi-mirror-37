# -*- coding: utf-8 -*-

import json

from .base import BaseSCenterAPI


class Delivery(BaseSCenterAPI):
    path = 'ec_deliverys/'

    def get(self, id=None):
        """
        :param slug:
        :return:
        """
        return self._get("{}{}/".format(self.path, id)).json()

    def update(self, id, data):
        return self._patch("{}{}/".format(self.path, id), json=data).json()

    def receive(self, slug, data):
        path = self.path + slug + '/receive/'
        return self._post(path, json=data).json()

    def refuse(self, slug, data):
        path = self.path + slug + '/refuse/'
        return self._post(path, json=data).json()