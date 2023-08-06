from eth_tool.connector import Connector
import os


web3_connect_type = os.getenv("web3_connect_type")
web3_connect_address = os.getenv("web3_connect_address")
web3_testnet = os.getenv("web3_testnet")

if not web3_connect_type or not web3_connect_address or not web3_testnet:
    raise Exception('请在环境变量里设置web3连接方式')

web3_connector = Connector(web3_connect_type, web3_connect_address, web3_testnet)
