# -*- coding: utf-8 -*-

from .base import BaseSCenterAPI


class PartnerRelation(BaseSCenterAPI):
    path = 'ec_partnerrelations/'

    def agree(self, id=None):
        path = self.path + '{}/agree/'.format(id)
        return self._post(path).json()

    def get(self, id=None):
        """
        :param slug:
        :return:
        """
        return self._get('{}{}/'.format(self.path, id)).json()

    def list(self, page=1):
        """
        :param page: 页码
        :return:
        """
        params = {'page': page}
        return self._get(self.path, params=params).json()
