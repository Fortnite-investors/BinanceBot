import decimal
from modules import p2p_converter

import pytest


async def test_converter(mock_binance, load_json):
    @mock_binance('v2/friendly/c2c/adv/search')
    def _mock(host, url, method, body):
        if body['tradeType'] == 'SELL':
            return load_json('search_sell_for_try.json')
        return load_json('search_response.json')

    result = await p2p_converter.module.calc_convert_price(
        decimal.Decimal(500), 'TRY', 'ZIRAAT', 'RUB', 'TINKOFF'
    )

    assert result
    assert result.mean_buy_price == decimal.Decimal('73.37')
    assert result.mean_sell_price == decimal.Decimal('16.25')
    assert result.total_price == decimal.Decimal('2275')


async def test_small_amount(mock_binance, load_json):
    @mock_binance('v2/friendly/c2c/adv/search')
    def _mock(host, url, method, body):
        if body['tradeType'] == 'SELL':
            return load_json('search_sell_for_try.json')
        return load_json('search_response.json')

    with pytest.raises(p2p_converter.exceptions.ConvertError):
        await p2p_converter.module.calc_convert_price(
            decimal.Decimal(1), 'TRY', 'ZIRAAT', 'RUB', 'TINKOFF'
        )

async def test_binance_error(mock_binance):
    @mock_binance('v2/friendly/c2c/adv/search')
    def _mock(host, url, method, body):
        raise Exception('ololo')

    with pytest.raises(p2p_converter.exceptions.ConvertError):
        await p2p_converter.module.calc_convert_price(
            decimal.Decimal(1), 'TRY', 'ZIRAAT', 'RUB', 'TINKOFF'
        )
