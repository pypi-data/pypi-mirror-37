# coding=utf-8

from .base import BaseSCenterAPI


class ProductShelvesStatus(BaseSCenterAPI):
    path = 'ec_productshelvesstatuss/'

    def create(self, data):
        """
        :param data:
        :return:
        """
        return self._post(self.path, json=data).json()

    def update(self, slug, data):
        """
        :param slug:
        :param data:
        :return:
        """
        return self._patch("{}{}/".format(self.path, slug), json=data).json()

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

    def down(self, slug):
        return self._post('{}{}/down/'.format(self.path, slug)).json()
