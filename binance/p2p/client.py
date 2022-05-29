import asyncio
import decimal

from .. import base_client
from . import models

from typing import List

BASE_URL = 'https://p2p.binance.com/bapi/c2c/'

class Client(base_client.Client):
    _client: base_client.Client
    
    def __init__(self, api_key: str, secret_key: str):
        self._client = base_client.Client(api_key, secret_key)
    
    async def search(
        self, asset: str, fiat: str, tradetype: str, 
        paytypes = [], transAmount: decimal.Decimal = None, limit: int = 20
    ) -> List[models.Data]:
        url = 'v2/friendly/c2c/adv/search'

        result = []
        for page in range(0, max(1, limit // 20)):
            body = {
                'asset': asset,
                'fiat': fiat,
                'merchantCheck': False,
                'page': page + 1,
                'payTypes': paytypes,
                'publisherType': None,
                'rows': 20,
                'tradeType': tradetype
            }

            if transAmount:
                body.update({'transAmount': str(transAmount)})

            response = await self._client.make_request(
                BASE_URL, url, method='POST', body=body
            )
            if response:
                for elem in response['data']:
                    result.append(models.Data.from_dict(elem))
            await asyncio.sleep(0.1)

        return result
