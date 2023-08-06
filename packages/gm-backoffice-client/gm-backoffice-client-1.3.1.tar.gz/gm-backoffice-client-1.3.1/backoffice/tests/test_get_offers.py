import pytest
import requests_mock

from ..http import BackofficeHTTPException


@pytest.mark.parametrize('api_data', (
    [
        {
            'id': 100,
            'site_id': 128,
            'name': 'Камаз с пирожками',
            'offers': [
                {
                    'partner_id': 'b',
                    'price': 100500,
                },
                {
                    'partner_id': 'd',
                    'price': 100501,
                },
            ],
        },
        {
            'id': 234,
            'site_id': 256,
            'name': 'Ведро с тестами',
            'offers': [
                {
                    'partner_id': 'e',
                    'price': 100503,
                },
                {
                    'partner_id': 'f',
                    'price': 100504,
                },
            ],
        },
    ],
))
def test_url(api_data, backoffice):
    with requests_mock.mock() as m:
        m.get('http://testhost/products/offers/?site_ids=128,256', status_code=200, json=api_data)

        assert backoffice.get_offers([128, 256]) == api_data


def test_cashless(backoffice):
    with requests_mock.mock() as m:
        m.get('http://testhost/products/offers/?cashless=1&site_ids=128,256', status_code=200, json={'a': 'b'})

        assert backoffice.get_offers([128, 256], cashless=True) == {'a': 'b'}


def test_non_200_response_to_product_offers_stat_get(backoffice):
    with requests_mock.mock() as m:
        m.get('http://testhost/products/offers/?site_ids=128,256', status_code=404)

        with pytest.raises(BackofficeHTTPException):
            assert backoffice.get_offers([128, 256])
