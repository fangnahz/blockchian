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

    def new_transaction(self, sender, recipient, amount):
        '''
        在区块中增加一条交易记录
        :param sender: <str> 发出方地址
        :param recipient: <str> 接收方地址
        :param amount: <int> 金额
        :return <int> 记录这条交易的区块的序号
        '''
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.last_block['index'] + 1  # 下一个挖矿目标的区块序号

    @staticmethod
    def hash(block):
        # 计算一个区块的哈希值
        pass

    @property
    def last_block(self):
        # 返回区块链的最后一个区块
        pass
