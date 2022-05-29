import binance

import pytest


@pytest.mark.parametrize('response, size', [
    ('search_response.json', 10),
    ('search_empty_response.json', 0)
])
async def test_p2p_list(mock_binance, load_json, response, size):
    @mock_binance('v2/friendly/c2c/adv/search')
    def _mock(host, url, method, body):
        assert body == {
            'asset': 'USDT', 
            'fiat': 'RUB', 
            'merchantCheck': False, 
            'page': 1, 
            'payTypes': [], 
            'publisherType': None, 
            'rows': 20, 
            'tradeType': 'BUY'
        }
        return load_json(response)

    binance_client = binance.module.BinanceClient()
    res = await binance_client.p2p.search(asset='USDT', fiat='RUB', tradetype='BUY')
    assert len(res) == size
