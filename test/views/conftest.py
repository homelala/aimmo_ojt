import pytest


@pytest.fixture
def headers(token):
    if token:
        headers = {"token": token}
    else:
        headers = None
    return headers
