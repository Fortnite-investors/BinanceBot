import decimal
import logging
import math
import statistics
import sys
from typing import Optional, List

import binance

from . import models
from . import exceptions


logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


def _filter_offers_by_amount(
    offers: List[binance.module.p2p.models.Data], amount: decimal.Decimal
) -> List[binance.module.p2p.models.Data]:
    result = []

    for offer in offers:
        if amount >= offer.offer.minSingleTransAmount and amount <= offer.offer.maxSingleTransAmount:
            result.append(offer)
    
    return result


def _filter_offers_by_asset(
    offers: List[binance.module.p2p.models.Data], asset_amount: decimal.Decimal):
    result = []

    for offer in offers:
        fiat_sum = asset_amount * offer.offer.price
        if fiat_sum >= offer.offer.minSingleTransAmount and fiat_sum <= offer.offer.maxSingleTransAmount:
            result.append(offer) 
    
    return result

async def calc_convert_price(
    goal_amount, goal_currency, goal_bank, base_currency, base_bank
) -> Optional[models.ConvertResult]:
    binance_client = binance.module.BinanceClient()

    logger.info(f'requesting offers to sell for {goal_currency} and bank {goal_bank}')
    try:
        sell_offers = await binance_client.p2p.search(
            asset='USDT', fiat=goal_currency, tradetype='SELL', paytypes=[goal_bank], 
            limit=20,
        )
    except Exception as e:
        logger.error('binance error ' + str(e))
        raise exceptions.ConvertError(f'Ошибка при запросе в binance')

    logger.info(f'filtering offers for {goal_amount} {goal_currency}')
    filtered_sell_offers = _filter_offers_by_amount(sell_offers, goal_amount)
    if not filtered_sell_offers:
        raise exceptions.ConvertError(f'Не удалось найти продавцов для {goal_amount} {goal_currency}')


    best_sell_rate = filtered_sell_offers[0].offer.price

    logger.info(f'best sell rate for {goal_currency} is {best_sell_rate}')

    usdt_amount = math.ceil(goal_amount / best_sell_rate)

    logger.info(f'requesting offers to buy for {base_currency} and bank {base_bank}')

    try:
        buy_offers = await binance_client.p2p.search(
            asset='USDT', fiat=base_currency, tradetype='BUY', paytypes=[base_bank],
            limit=20,
        )
    except Exception as e:
        logger.error('binance error ' + str(e))
        raise exceptions.ConvertError(f'Ошибка при запросе в binance')

    logger.info(f'filtering offers for {usdt_amount} USDT')
    filtered_buy_offers = _filter_offers_by_asset(buy_offers, usdt_amount)
    if not filtered_buy_offers:
        raise exceptions.ConvertError(f'Не удалось найти продавцов для {usdt_amount} USDT в {base_currency}')
    
    best_buy_rate = filtered_buy_offers[0].offer.price

    logger.info(f'best sell rate for {base_currency} is {best_buy_rate}')

    return models.ConvertResult(
        best_buy_rate, #statistics.mean([offer.offer.price for offer in filtered_buy_offers]),
        best_sell_rate, #statistics.mean([offer.offer.price for offer in filtered_sell_offers]),
        math.ceil(best_buy_rate * usdt_amount)
    )
