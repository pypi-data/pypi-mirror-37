import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.dialects.sqlite import NUMERIC
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
path = os.getenv("data_dir") + 'eth/'
engine = create_engine('sqlite:///' + path + 'wallet.db')
DBSession = sessionmaker(bind=engine)

session = DBSession()


class Address(Base):
    # 地址表:
    __tablename__ = 'address'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    address = Column(String(256), nullable=False)
    account = Column(String(40), nullable=False, server_default="")
    private_key = Column(String(2), nullable=False, server_default="")


class Transactions(Base):
    """交易表"""
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    transaction_hash = Column(String(256), nullable=False)
    block_hash = Column(String(256), nullable=False)
    block_number = Column(Integer, nullable=False)
    transaction_index = Column(Integer, nullable=True)
    account = Column(String(40), nullable=False, server_default="")
    category = Column(String(10), nullable=False)
    from_address = Column(String(256), nullable=False)
    to_address = Column(String(256), nullable=False)
    value = Column(NUMERIC(30, 15), nullable=False)
    fee = Column(NUMERIC(30, 15), nullable=False)
    status = Column(Integer, nullable=True)


def init_db():
    """
    初始化数据库
    :return:
    """
    db_name = 'wallet.db'
    path = os.getenv("data_dir") + 'eth/'
    if not os.path.exists(path):
        os.mkdir(path)

    url = os.path.join(path + db_name)

    if not os.path.exists(url):
        Base.metadata.bind = engine
        Base.metadata.create_all()


import re, importlib


class CommonService(object):
    _model = None
    _error = None

    def __init__(self):

        super(CommonService, self).__init__()
        if not self._model:
            model_name = re.sub('Service$', '', self.__class__.__name__)
            models = importlib.import_module('eth_tool.db')
            self._model = getattr(models, model_name)
        self.columns = [t.name for t in self._model.__table__.columns]
        print(self.columns)

    def get_data(self, where=None):

        data = session.query(self._model)
        if where == None:
            where = {}

        if isinstance(where, int) or isinstance(where, list):
            where = {'id': where}

        for key, value in where.items():
            if value is not None:
                if isinstance(value, list):
                    data.filter(getattr(self._model, key).in_(value))

                elif isinstance(value, dict):
                    for vk, vv in value:
                        if vv is not None:
                            operators = ['lt', 'gt', 'eq', 'le', 'ge', 'ne']
                            operator = '__{}__'.format(vk) if vk in operators else vk
                            operate = getattr(getattr(self._model, key), operator)
                            if isinstance(vv, list):
                                expression = operate(*vv)
                            else:
                                expression = operate(vv)

                            data = data.filter(expression)

        return data

    def __getattr__(self, item):
        if item.startswith('get_by_'):
            field_name = re.sub("^get_by_", '', item)
            if field_name in self.columns:
                def get_by_filed(value):
                    data = self.get_data({field_name: value})
                    return data.all()

                return get_by_filed


class TransactionsService(CommonService):
    pass
