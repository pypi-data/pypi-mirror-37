import inspect
from typing import Callable, Generator, Iterable, List, Union

from . import processors
from .http import BackofficeHTTP
from .orders import BackofficeOrderValidator


class BackofficeException(BaseException):
    pass


class BackofficeClient:
    def __init__(self, url: str, token: str):
        self.validator = BackofficeOrderValidator()
        self.processor = BackofficePreprocessor()
        self.http = BackofficeHTTP(url, token)

    def send(self, order: dict, items: List):
        """Preprocess, validatate and send an order to the backoffice API"""
        order = self.processor.run_processors(order, 'order')
        self.validator.validate_order(order)

        order = self._post_order(order)
        if 'id' not in order.keys():
            raise BackofficeException('Incorrect response from backoffice (no order id)')

        items = self.processor.run_processors(items, 'items')
        self.validator.validate_items(items)
        self._post_items(order, items)
        return order

    def send_lead(self, lead: dict) -> dict:
        """Send lead to the backoffice"""

        if not lead.get('email') and not lead.get('phone'):
            raise ValueError('Email or phone is required')

        return self.http.post('leads', lead)

    def _post_order(self, order: dict) -> dict:
        """Send order to the backoffice"""
        return self.http.post('orders', order)

    def _post_items(self, order: dict, items: List):
        """Send order items to the backoffice, given an order"""
        return self.http.post('orders/{order_id}/items/'.format(order_id=order['id']), items)

    def get_price(self, site_id: int) -> dict:
        """Get price from the price list"""
        return self.http.get('price_lists/sell/{site_id}/'.format(site_id=site_id))

    def get_products_sales_stat(self, site_ids: List[Union[str, int]]) -> Iterable:
        """Get product sales statistics"""
        return self._get_data_by_site_ids('products/sales_stat/?site_ids={site_ids}', site_ids)

    def get_products_offers_stat(self, site_ids: List[Union[str, int]]) -> Iterable:
        """Get partner offer statistics"""
        return self._get_data_by_site_ids('products/offers_stat/?site_ids={site_ids}', site_ids)

    def get_products_orders_stat(self, site_ids: List[Union[str, int]]) -> Iterable:
        """Get partner order statistics"""
        return self._get_data_by_site_ids('products/orders_stat/?site_ids={site_ids}', site_ids)

    def get_offers(self, site_ids: List[Union[str, int]], cashless=False) -> Iterable:
        """Get current offers of all partners (for the warehouse)"""
        if cashless:
            url = 'products/offers/?cashless=1&site_ids={site_ids}'
        else:
            url = 'products/offers/?site_ids={site_ids}'

        return self._get_data_by_site_ids(url, site_ids)

    def _get_data_by_site_ids(self, url, site_ids: List[Union[str, int]]) -> dict:
        site_ids_str = ','.join([str(el) for el in site_ids])

        return self.http.get(url.format(url, site_ids=site_ids_str))


class BackofficePreprocessor:
    @classmethod
    def run_processors(cls, obj, what: str):
        """Runs the processors defined in processors.py.

        What may be an 'order' or 'item'
        """
        for processor in cls.get_processors(what):
            obj = processor(obj)
            if obj is None:
                raise AttributeError(f'Processor {processor} returned nothing!')

        return obj

    @staticmethod
    def get_processors(what: str) -> Generator[Callable, None, None]:
        for member in inspect.getmembers(processors, lambda member: inspect.isfunction(member) and what in inspect.signature(member).parameters.keys()):
            yield member[1]
