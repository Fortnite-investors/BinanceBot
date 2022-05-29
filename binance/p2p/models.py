import decimal
from typing import List, NamedTuple


class TradeMethod(NamedTuple):
    payType: str
    identifier: str

class Offer(NamedTuple):
    tradeType: str
    asset: str
    fiatUnit: str
    price: decimal.Decimal
    initAmount: decimal.Decimal
    maxSingleTransAmount: decimal.Decimal
    minSingleTransAmount: decimal.Decimal
    tradeMethods: List[TradeMethod]

    @staticmethod
    def from_dict(d: dict):
        return Offer(
            tradeType=d['tradeType'],
            asset=d['asset'],
            fiatUnit=d['fiatUnit'],
            price=decimal.Decimal(d['price']),
            initAmount=decimal.Decimal(d['initAmount']),
            maxSingleTransAmount=decimal.Decimal(d['maxSingleTransAmount']),
            minSingleTransAmount=decimal.Decimal(d['minSingleTransAmount']),
            tradeMethods=[TradeMethod(**i) for i in d['tradeMethods']]
        )

class Data(NamedTuple):
    offer: Offer

    @staticmethod
    def from_dict(d: dict):
        return Data(
            offer=Offer(d['adv'])
        )
