from test.env import *
from eth_tool.chain import Chain
chain=Chain()
block=chain.get_block_by_number(3181330)
block_info=block.get_block_details()
print(block_info)
