import pytest


@pytest.mark.parametrize('input, param, value, expected', [
    ['/test/create', 'par1', 'val1', '/test/create?par1=val1'],
    ['/test/create?par1=DELETED', 'par1', 'val1', '/test/create?par1=val1'],  # overwriting params
    ['/test/create/?par2=val2', 'par1', 'val1', '/test/create/?par2=val2&par1=val1'],
])
def test_append_qs(input, param, value, expected, backoffice):
    assert backoffice.http._append_qs(input, param, value) == expected
