import pytest
import requests_mock

from ..http import BackofficeHTTPException


def test_order_url(backoffice):
    with requests_mock.mock() as m:
        m.post('http://testhost/orders/', status_code=201, json={'mock': 'mmmock'})
        assert backoffice._post_order('some stuff') == {'mock': 'mmmock'}


def test_non_201_response_to_order_post(backoffice):
    with requests_mock.mock() as m:
        m.post('http://testhost/orders/', status_code=403)
        with pytest.raises(BackofficeHTTPException):
            backoffice._post_order('some stuff')


def test_items_url(backoffice):
    with requests_mock.mock() as m:
        m.post('http://testhost/orders/100500/items/', status_code=201, json={'mock': 'mmmock'})
        assert backoffice._post_items({'id': 100500}, [{'mo': 'ck'}]) == {'mock': 'mmmock'}


def test_non_201_response_to_items_post(backoffice):
    with requests_mock.mock() as m:
        m.post('http://testhost/orders/100500/items/', status_code=403)
        with pytest.raises(BackofficeHTTPException):
            backoffice._post_items({'id': 100500}, [{'mo': 'ck'}])
