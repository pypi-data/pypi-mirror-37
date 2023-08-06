因为geth 没有提供listtransactions 用来快速查阅自己账号的交易记录.
首先导入环境变量

os.environ["web3_connect_type"] = "HTTPProvider" #连接类型
os.environ["web3_connect_address"] = "连接地址"
os.environ["web3_testnet"] = "是否为测试网,1表示是"
os.environ["data_dir"] = "把交易历史记录写到特定目录下"

接着实例化Manager类
manager = Manager()
datas = manager._get_transactions_by_number(3181592)
manager.scan_block('我们关注的地址')





