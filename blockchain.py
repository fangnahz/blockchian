# coding: utf-8
import hashlib
import json
import time
import uuid


class Blockchain(object):
    '''
    负责管理区块链，存储交易记录，提供增加区块的方法
    '''
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)  # 新建初始区块 (genesis block)

    def new_block(self, proof, previous_hash=None):
        '''
        在区块链中新建区块
        :param proof: <int> 工作证明算法提供的证明
        :param previous_hash: (Optional) <str> 上一个区块的哈希
        :return: <dict> 新区块
        '''
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        self.current_transactions = []  # 重置当前交易记录
        self.chain.append(block)
        return block

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
        return self.last_block['index'] + 1  # 下一个挖矿目标的区块序号，后面提交交易记录时需要用到

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        '''
        创建一个区块的 SHA-256 哈希
        :param block: <dict> Block
        :return: <str>
        '''
        block_string = json.dumps(block, sort_keys=True).encode('utf-8')  # 排序序列化确保同一个字典哈希结果一致
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        '''
        简单的 PoW 算法：
         - 找到数字 p'，让 hash(p * p') 开始四位为 0，其中 p 是上一轮的 p'
         - p 是上一轮的 proof，p' 是新 proof
        :param last_proof: <int>
        :return: <int>
        '''
        proof = 0  # 从零开始，直到找到满足条件的数字
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        '''
        验证 proof: 检查 hash(last_proof, proof) 开头四位是不是 0
        :param last_proof: <int> 上一轮的 proof
        :param proof: <int> 当前 proof
        :return: <bool> 正确为 True，否则为 False
        '''
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'
