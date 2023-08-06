import pytest
import requests_mock

from ..http import BackofficeHTTPException


@pytest.mark.parametrize('url', [
    '/partners/',
    '/partners',
    'partners/',
    'partners',
])
def test_200(url, backoffice):
    with requests_mock.mock() as m:
        m.get('http://testhost/partners/', status_code=200, json={'__mocked': True})

        assert backoffice.http.get(url) == {'__mocked': True}


def test_404(backoffice):
    with requests_mock.mock() as m:
        m.get('http://testhost/partners/', status_code=404)

        with pytest.raises(BackofficeHTTPException):
            backoffice.http.get('partners')
