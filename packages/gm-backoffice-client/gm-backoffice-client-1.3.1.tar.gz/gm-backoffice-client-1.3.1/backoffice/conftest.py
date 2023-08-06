import json

import pytest

from .client import BackofficeClient


@pytest.fixture
def backoffice():
    return BackofficeClient(
        url='http://testhost',
        token='tsttkn',
    )


@pytest.fixture
def response():
    """Fixture reader"""
    def read_file(fname):
        with open('./backoffice/tests/fixtures/' + fname + '.json') as fp:
            return json.load(fp)

    return read_file
