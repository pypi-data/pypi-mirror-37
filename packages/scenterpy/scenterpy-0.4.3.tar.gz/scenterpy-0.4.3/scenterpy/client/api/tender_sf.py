# -*- coding: utf-8 -*-

import json

from .base import BaseSCenterAPI


class TenderSf(BaseSCenterAPI):
    path = 'tender_tendersfs/'

    def cancel(self, data):
        path = self.path + 'cancel/'
        return self._post(path, json=data).json()

    def create(self, data):
        path = self.path + 'tendersf/'
        return self._post(path, json=data).json()

    def bidding(self, data):
        path = self.path + 'bidding/'
        return self._post(path, json=data).json()


class TenderSfRound(BaseSCenterAPI):
    path = 'tender_tendersfrounds/'

    def updatetime(self, data):
        path = self.path + 'updatetime/'
        return self._post(path, json=data).json()

    def create(self, data):
        path = self.path + 'newround/'
        return self._post(path, json=data).json()

    def submit(self, data):
        path = self.path + 'submit/'
        return self._post(path, json=data).json()