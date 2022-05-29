import json
import os

import pytest

from binance import base_client

@pytest.fixture
def mock_binance(monkeypatch):
    def dec(mocked_url):
        def decorator(func):
            async def mock_request(obj, host, url, *args, **kwargs):
                if (url == mocked_url):
                    return func(host, url, *args, **kwargs)
                raise ValueError(f'uknown handler {url}')
            
            monkeypatch.setattr(base_client.Client, "make_request", mock_request)

        return decorator
    return dec


@pytest.fixture
def load_json():
    def open_and_load(filename):
        if filename in os.listdir('tests/static'):
            with open('tests/static/' + filename, 'r') as f:
                return json.loads(f.read())
        raise ValueError('File not found')

    return open_and_load
