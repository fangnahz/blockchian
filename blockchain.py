# coding: utf-8


class Blockchain(object):
    '''
    负责管理区块链，存储交易记录，提供增加区块的方法
    '''
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def new_block(self):
        # 在区块链中新建、增加一个区块
        pass

    def new_transaction(self):
        # 在交易记录中增加一条记录
        pass

    @staticmethod
    def hash(block):
        # 计算一个区块的哈希值
        pass

    @property
    def last_block(self):
        # 返回区块链的最后一个区块
        pass
