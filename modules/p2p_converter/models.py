import decimal
from typing import NamedTuple


class ConvertResult(NamedTuple):
    mean_buy_price: decimal.Decimal
    mean_sell_price: decimal.Decimal
    total_price: decimal.Decimal
