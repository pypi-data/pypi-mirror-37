import pytest
import requests_mock

from ..http import BackofficeHTTPException


def test_non_201_response_to_lead_post(backoffice):
    with requests_mock.mock() as m:
        m.post('http://testhost/leads/', status_code=403)
        with pytest.raises(BackofficeHTTPException):
            backoffice.send_lead({'email': 'test@example.com'})


def test_params_email_or_phone_is_required(backoffice):
    with requests_mock.mock() as m:
        m.post('http://testhost/leads/', status_code=201)
        with pytest.raises(ValueError):
            backoffice.send_lead({})


@pytest.mark.parametrize('payload', (
    {'email': 'test@example.com'},
    {'phone': '+7 999 999-99-99'},
))
def test_send_lead(backoffice, payload):
    with requests_mock.mock() as m:
        m.post('http://testhost/leads/', status_code=201, json={'mock': 'mmmock'})

        assert backoffice.send_lead(payload) == {'mock': 'mmmock'}


@pytest.mark.parametrize('utm', (
    {},
    {'utm_source': '100500'},
    {'utm_source': '100500', 'utm_medium': '100500'},
))
def test_lead_utm(backoffice, utm):
    utm.update({'email': 'test@example.com'})

    with requests_mock.mock() as m:
        m.post('http://testhost/leads/', status_code=201, json={'mock': 'mmmock'})
        backoffice.send_lead(utm)

        assert m.last_request.json() == utm
