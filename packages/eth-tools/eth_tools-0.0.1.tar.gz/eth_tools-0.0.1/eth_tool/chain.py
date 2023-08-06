import os
from eth_tool import web3_connector
from eth_tool.block import Block


class Chain:

    def get_address_by_path(self, path="./"):
        """
        根据文件路径获取地址
        :param path:
        :return:
        """
        if not os.path.exists(path):
            return []
        address_file = [file_name for file_name in os.listdir(path) if os.path.isfile(file_name)]
        address_list = []
        for file_name in address_file:
            *other, address = file_name.split("--")
            address = "0x" + address
            address_list.append(address)

        return address_list

    def get_last_block(self):
        """
        获取最新的区块
        :return:
        """
        block_info = web3_connector.eth.getBlock("latest")
        return block_info

    def get_accounts(self):
        return web3_connector.eth.accounts

    def get_block_number(self):
        """
        返回当前区块号
        :return:
        """
        data = web3_connector.eth.blockNumber
        return data

    def get_block_by_number(self, number):
        """
        根据区块号获取区块
        :param number: 区块号
        :return: Block
        """
        block = Block(number)
        return block

    def get_block_by_hash(self, block_hash):
        """
        根据block_hash获取区块
        :param block_hash:
        :return:
        """
        try:
            block_info = web3_connector.getBlock(block_hash)
            return self.get_block_by_number(block_info['number'])
        except Exception:
            raise Exception("NOT FOUND BLOCK BY %s" % (block_hash))

    def has_block(self, block):
        """
        判断是否存在该区块
        :param block: 区块hash 或者 区块号
        :return:
        """
        try:
            web3_connector.getBlock(block)
            return True
        except Exception:
            raise False

    def get_transaction_receipt(self, transaction_hash):
        """
        根据交易hash获取交易详情
        :param transaction_hash:
        :return:
        """
        return web3_connector.eth.getTransactionReceipt(transaction_hash)
