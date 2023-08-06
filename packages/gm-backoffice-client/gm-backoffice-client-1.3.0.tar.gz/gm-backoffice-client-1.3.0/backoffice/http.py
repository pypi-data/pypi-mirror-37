from collections import OrderedDict
from typing import Generator
from urllib.parse import parse_qsl, urljoin, urlparse, urlunparse

import requests


class BackofficeHTTPException(BaseException):
    pass


class BackofficeHTTP:
    headers = {
        'Authorization': 'Token {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    def __init__(self, host: str, token: str, timeout=6):
        self.host = host
        self.timeout = timeout
        self.headers['Authorization'] = self.headers['Authorization'].format(token=token)

    @staticmethod
    def _append_qs(url: str, key: str, value: str) -> str:
        """Append a parameter to the url querystring"""
        url = list(urlparse(url))
        query = OrderedDict(parse_qsl(url[4]))
        query[key] = value
        url[4] = '&'.join(f'{p}={v}' for p, v in query.items())

        return urlunparse(url)

    def paginate(self, url) -> Generator[dict, None, None]:
        next_page = self._append_qs(url, 'page', 1)
        while next_page is not None:
            response = self.get(next_page)

            for result in response.get('results', []):
                yield result

            next_page = response.get('next')

    def get(self, url: str):
        url = urljoin(self.host, url)
        if not url.endswith('/') and '?' not in url:
            url += '/'

        r = requests.get(url, headers=self.headers, timeout=self.timeout)

        if r.status_code != 200:
            raise BackofficeHTTPException(
                'Non-200 response when fetching url {}: {}'.format(url, r.status_code))

        return r.json()

    def post(self, url: str, payload: dict):
        url = urljoin(self.host, url)

        if not url.endswith('/'):
            url += '/'

        r = requests.post(url, json=payload, headers=self.headers, timeout=self.timeout)

        if r.status_code != 201:
            raise BackofficeHTTPException(
                'Non-201 response when posting to url {}: {}'.format(url, r.status_code))

        return r.json()
