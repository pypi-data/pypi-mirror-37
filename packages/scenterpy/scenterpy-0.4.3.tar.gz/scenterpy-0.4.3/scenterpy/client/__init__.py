from . import api
from .base import BaseSCenterClient


class SCenterClient(BaseSCenterClient):
    # API_BASE_URL = 'http://supplier.cognichain.com/api/v1/'

    @property
    def order(self):
        return api.BaseModelAPI(self, 'ec_orders/')

    @property
    def shelves_set(self):
        return api.BaseModelAPI(self, 'ec_shelvessets/')

    @property
    def shelves_set_item(self):
        return api.BaseModelAPI(self, 'ec_shelvesitems/')

    @property
    def aftersale_order(self):
        return api.BaseModelAPI(self, 'ec_aftersaleorders/')

    @property
    def product(self):
        return api.Product(self)

    @property
    def product_shelves_status(self):
        return api.ProductShelvesStatus(self)

    @property
    def common(self):
        return api.Common(self)

    @property
    def delivery(self):
        return api.Delivery(self)

    @property
    def tender_sf(self):
        return api.TenderSf(self)

    @property
    def tender_sf_round(self):
        return api.TenderSfRound(self)

    @property
    def partner(self):
        return api.Partner(self)
