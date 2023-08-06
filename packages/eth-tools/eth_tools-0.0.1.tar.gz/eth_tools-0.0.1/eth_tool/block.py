from eth_tool import web3_connector


class Block():
    def __init__(self, number):
        self.number = number
        try:
            self.block_info = web3_connector.eth.getBlock(number,True)
            self.number = number

        except Exception:

            raise Exception('NOT FOUND BLOCK BY %s' % (number))

    def get_block_details(self):
        """
        获取区块详情
        :param number:
        :return:
        """
        return self.block_info

    def get_transactions(self):
        """
        返回当前区块的交易列表
        :return:
        """
        block_info = self.get_block_details()
        transactions = block_info['transactions']
        return transactions

    def get_transaction_by_block(self, transaction_index):
        """
        获取指定区块的,transaction_index 值为transaction_index 的交易
        :param transaction_index:
        :return:
        """
        data = web3_connector.eth.getTransactionByBlock(self.number, transaction_index)
        return data


