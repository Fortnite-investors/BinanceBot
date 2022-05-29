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
        paytypes = [], limit: int = 10
    ) -> List[models.Data]:
        url = 'v2/friendly/c2c/adv/search'

        result = []
        for rows in range(0, limit, 10):
            body = {
                'asset': asset,
                'fiat': fiat,
                'merchantCheck': False,
                'page': rows // limit + 1,
                'payTypes': paytypes,
                'publisherType': None,
                'rows': 10,
                'tradeType': tradetype
            }
            response = await self._client.make_request(
                BASE_URL, url, method='POST', body=body
            )
            if response:
                for elem in response['data']:
                    result.append(models.Data(elem))
        
        return result
