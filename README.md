# 原作者 [Daniel Von Flymen](https://github.com/dvf/)，[原代码](https://github.com/dvf/blockchain)，[原文](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)

# 区块链玩具项目

## 加密货币 (Cryptocurrency)
设计初衷是交易的媒介，核心是被强加密保护的帐本。

## 区块链 (Blockchain)
区块链是区块 (Block) 构成的**不可变、有序链**。

常说的比特币等加密货币是去中心化 (分布式) 系统，区块链是实现分布式帐目数据库记录的技术。

区块可以包含交易记录，成为一个分布式帐本 (Distributed Ledger)，这样的系统实现的就是加密货币。

区块也可以包括文件或任何数据，实现任何基于信任行为的系统设计。区块链技术把人与人之间的信任问题，转换成了计算问题 (by C.B.)。

区块使用哈希链接在一起，构成区块链。

哈希实现了在不泄漏区块中数据的前提下数据一致性的证明。

区块应该包含序号 (Index), 时间戳 (timestamp), 交易记录列表 (transactions), 证明 (proof), 上一个区块的哈希。下面是一个具体的示例：

```python
block = {
    'index': 1,
    'timestamp': 1533864345.644769,
    'transactions': [
        {
            'sender': '0a367b92cf0b037dfd89960ee832d56f',
            'recipient': '665d0698dbc8fb95afc25c3a4d9cf280',
            'amount': 2
        }
    ],
    'proof': 347913885878,
    'previous_hash': '2fdf0351e5959fab118beb6014be394d921a616d580a71056682120f7c9c1911'
}
```

类似于数据结构中的链表，区块链中的每一个区块包含了可以唯一确认上一个区块的哈希值 `previous_hash`。

通过这个哈希值，区块被链接在一起，所以叫区块链。

这个哈希值是区块链技术的关键点：
区块间用哈希关联，让区块链变成了**不可变**的数据结构。如果任何一个区块被改变，比如被入侵修改，该区块的哈希值就会变化，
这个区块之后**所有**区块的 `previous_hash` 都变成了错误的哈希值。

## **P**roof **o**f **W**ork (PoW)
前面提到的 “证明 (proof)”

PoW：找到解决一个问题的数字

算法要难计算，容易验证

一个具体的例子：某个整数乘以另一个整数的哈希最后一位是 0

```python
import hashlib

x = 5
y = 0  # 从零开始，计算符合要求的数字

while hashlib.sha256(f'{x*y}'.encode('utf-8')).hexdigest()[-1] != '0':
    y += 1

print(f'The solution is y = {y}')
```

比特币的 PoW 算法是 [Hashcash](https://en.wikipedia.org/wiki/Hashcash)。

## 记录交易 endpoint
下面是用户提交给服务器的交易请求数据的一个例子：

```
{
    "sender": "my adress",
    "recipient": "someone else's adress",
    "amount": 5
}
```

## 挖矿 endpoint
需要做三件事：
1. 计算 PoW
2. 奖励矿工（转帐 1 个 coin）
3. 把新区块加入区块链中


## 共识
区块链的核心目的是去中心化，需要
**共识算法**来保证所有结点反映的是同一个区块链

首先，需要让一个结点能够记录网络中其他结点：在 Blockchain 类中增加记录所有结点的实例变量，增加更新结点列表的方法

增加新 endpoint 用于更新结点列表

增加新 endpoint 用于解决冲突，保证结点存储的是正确的区块链

### 冲突
一个结点保存的区块链与另一个结点不同时，判定合法区块链的方案。解决的原则比如：以最长的合法区块链为准。
解决冲突的方法会轮询网络中所有结点，下载每个结点的区块链，验证是否合法，如果找到新的更长的合法区块链，就用找到的区块链替换当前结点的区块链。
