from eth_tool.db import Address, Transactions, init_db
from eth_tool.chain import Chain
from eth_tool.db import session
from eth_tool import web3_connector


from web3.utils.encoding import (
    to_hex,
)

import os


class Manager:
    def __init__(self, start_block_number=None, config_block=10):
        init_db()
        block_chain = Chain()
        lost_block = block_chain.get_block_number()
        self.start_file = os.getenv("data_dir") + 'eth/start.txt'

        if not os.path.exists(self.start_file):
            self.start_number = start_block_number if start_block_number else lost_block - config_block

        else:
            self.start_number = self._get_block_num_by_file()

        self.end_number = lost_block - config_block

    def has_transaction(self, address, number):
        """
        查询指定区块的,是否有我们指定的的地址
        :param address:
        :param number:
        :return:
        """
        transaction_list = self._get_transactions_by_number(number)
        address_list = address if isinstance(address, list) else [address]
        send_transaction = self._get_transactions_by_action(address_list, transaction_list, 'from')
        reception = self._get_transactions_by_action(address_list, transaction_list, 'to')
        return send_transaction, reception

    def _get_transactions_by_number(self, number):
        """
        根据区块号获取交易记录
        :param number:
        :return:
        """
        block_chain = Chain()
        block = block_chain.get_block_by_number(number)
        return block.get_transactions()

    def _get_transactions_by_action(self, address_list, transaction_list, action):
        """
        查看匹配的地址的交易记录
        :param address_list:
        :param transaction_list:
        :param action:
        :return:
        """
        category_type = {
            "from": "send",
            "to": "receive"
        }
        my_transaction_list = []
        for address in address_list:
            for transaction in transaction_list:
                if address == transaction.get(action):
                    transaction = dict(transaction)
                    transaction['category'] = category_type.get(action)
                    self._write_transactions_to_db(transaction)
                    my_transaction_list.append(transaction)

        return my_transaction_list

    def _write_transactions_to_db(self, transaction):
        """
        把交易数据写入到数据库里
        :param transaction:
        :return:
        """
        data = Transactions(
            transaction_hash=str(to_hex(transaction.get('hash'))),
            block_hash=str(to_hex(transaction.get('blockHash'))),
            block_number=transaction.get('blockNumber'),
            transaction_index=transaction.get('transactionIndex'),
            category=transaction.get('category'),
            from_address=transaction.get('from'),
            to_address=transaction.get('to'),
            value=transaction.get('value'),
            fee=transaction.get('gas'),
        )

        session.add(data)
        session.commit()

    def _write_block_num_to_file(self, number):
        with open(self.start_file, "w") as fp:
            fp.write(str(number))

    def _get_block_num_by_file(self):
        with open(self.start_file, "r") as fp:
            block_num = fp.read()

        return int(block_num)

    def scan_block(self, address):
        current_number = self.start_number

        while current_number <= self.end_number:
            self.has_transaction(address, current_number)
            current_number = current_number + 1
            self._write_block_num_to_file(current_number)
