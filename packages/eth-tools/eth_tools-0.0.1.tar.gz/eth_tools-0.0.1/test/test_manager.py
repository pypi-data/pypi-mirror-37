from test.env import *
from eth_tool.manager import Manager

manager = Manager()
datas = manager._get_transactions_by_number(3181592)

manager.scan_block(
    ['0x05420fDd19F88D980Bf04be0E594FFE4C9B70171', '0xA83ebA054A5d3db45d359b8867D20E05a6D2FCEB'])

