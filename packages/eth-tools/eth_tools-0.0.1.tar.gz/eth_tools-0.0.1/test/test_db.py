from test.env import *
from eth_tool.db import *

transactions_srv=TransactionsService()
datas=transactions_srv.get_by_block_number(3198783)
for data in datas:
    print(data.fee)