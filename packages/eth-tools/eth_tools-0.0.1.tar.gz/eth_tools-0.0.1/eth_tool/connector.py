from web3.middleware import geth_poa_middleware
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import web3


class Connector():

    def __init__(self, connect_type, connect_address, testnet=False):

        connect_types = ['IPCProvider', 'HTTPProvider', 'WebsocketProvider']
        if not connect_type in connect_types:
            raise Exception("invalid connect type")
        provider = getattr(web3, connect_type)
        self.connettion = Web3(provider(connect_address))
        if testnet:
            self.connettion.middleware_stack.inject(geth_poa_middleware, layer=0)

    def __getattr__(self, item):
        return getattr(self.connettion, item)
