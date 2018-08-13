# coding: utf-8
import hashlib
import json
import requests
import time
import uuid
from textwrap import dedent
from urllib.parse import urlparse

from flask import Flask, jsonify, request


class Blockchain(object):
    '''
    负责管理区块链，存储交易记录，提供增加区块的方法
    '''
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)  # 新建初始区块 (genesis block)
        self.nodes = set()

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

    def register_node(self, address):
        '''
        在结点列表中新增结点
        :param address: <str> Address of node. e.g. 'http://192.168.0.5:5000'
        :return: None
        '''
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        '''
        检测给定的区块链是否合法
        :param chain: <list> 一个区块链
        :return: <bool> 合法为 True，否则为 False
        '''
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # 验证区块哈希是否正确
            if block['previous_hash'] != self.hash(last_block):
                return False
            # 验证 PoW 是否正确
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
        return True

    def resolve_conflicts(self):
        '''
        共识算法，用网络中最长区块链替换当前区块链
        :return: <bool> 如果当前区块链被替换则为 True，否则为 False
        '''
        neighbours = self.nodes
        new_chain = None
        # 寻找更长的区块链
        max_length = len(self.chain)
        # 获取、验证网络中其他所有结点的区块链
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                # 检查区块链是否更长且合法
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        # 如果发现新的更长的合法区块链，则替换当前结点区块链
        if new_chain:
            self.chain = new_chain
            return True
        return False


# 初始化结点
app = Flask(__name__)
# 生成结点的全局唯一地址
node_identifier = str(uuid.uuid4()).replace('-', '')
# 实例化区块链
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # 运行 PoW 算法获取下一个 Proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    # 找到 proof 以后获取奖励
    # sender 为 “0” 表示这个结点挖到了一个新 coin
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )
    # 把前面的转帐记录加入新建区块
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        'message': "new Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    # 验证 POST 请求包含了必要数据
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    # 创建新交易
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_node():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
    for node in nodes:
        blockchain.register_node(node)
    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
