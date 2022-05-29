from . import p2p

class BinanceClient:
    p2p: p2p.client.Client

    def __init__(self, api_key: str = '', secret_key: str = ''):
        self.p2p = p2p.client.Client(api_key, secret_key)

