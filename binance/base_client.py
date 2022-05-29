
import hashlib
import hmac
import json
import logging
import sys
import urllib.parse

import aiohttp


logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


class Client:
    def __init__(self, api_key: str = '', secret_key: str = ''):
        self._api_key = api_key
        self._secret_key = secret_key

    async def make_request(
            self,
            host: str,
            url: str,
            method: str = 'GET',
            args: dict = {},
            body: dict = {},
            signature: bool = False,
    ) -> dict:
        headers = {}
        if self._api_key:
            headers.update({'X-MBX-APIKEY': self._api_key})

        params = urllib.parse.urlencode(args)

        full_request = host + url
        if params:
            full_request = full_request + '?' + params
        logger.info(f'making {method} request {full_request} body = {body}')

        if signature:
            add_request = hmac.new(
                bytes(self._secret_key, 'utf-8'),
                bytes(params, 'utf-8'),
                hashlib.sha256,
            ).hexdigest()
            full_request += '&' + f'signature={add_request}'

        async with aiohttp.ClientSession() as session:
            if method.lower() == 'post':
                exec_method = session.post
            else:
                exec_method = session.get
            async with exec_method(full_request, headers=headers, json=body) as resp:
                logger.info(f'got response with status code = {resp.status}')
                body = await resp.text()
                if resp.status == 200:
                    body = await resp.text()
                    parsed_body = json.loads(body)
                    return parsed_body
        return None
