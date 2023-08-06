import pytest
import requests_mock


@pytest.fixture(autouse=True)
def mock_http_response(response):
    with requests_mock.mock() as m:
        m.get('http://testhost/products?page=1', json=response('products_1'))
        m.get('http://testhost/products?page=1', json=response('products_2'))

        yield


def test_ok(backoffice, response):
    got = list(backoffice.http.paginate('products'))

    assert len(got) == 25
