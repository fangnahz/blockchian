# 原作者 [Daniel Von Flymen](https://github.com/dvf/)，[原代码](https://github.com/dvf/blockchain), [原文](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)

# 区块链玩具项目

## 加密货币 (Cryptocurrency)
设计初衷是交易的媒介，核心是被强加密保护的账本。

## 区块链 (Blockchain)
区块链是区块 (Block) 构成的不可变、有序链。

常说的比特币等加密货币是去中心化 (分布式) 系统，区块链实现了系统的核心账本。

区块可以包含交易记录，成为一个分布式账本 (Distributed Ledger)，这样的系统实现的就是加密货币。

区块也可以包括文件或任何数据，实现任何基于信任行为的系统设计。区块链技术把人与人之间的信任问题，转换成了计算问题 (by C.B.)。

区块使用哈希链接在一起，就是区块链。

哈希实现了在不泄漏区块中数据的前提下数据一致性的证明。

区块应该包含序号 (Index), 时间戳 (timestamp), 交易记录列表 (transactions), 证明 (proof), 上一个区块的哈希。下面是一个具体的示例：

```python
block = {
    'index': 1,
    'timestamp': 1533864345.644769,
    'transactions': [
        {
            'sender': '2762754255d095f329ee779102423bdb',
            'recipient': '238255d947f5a440f200a561307e5fbf',
            'amount': 2
        }
    ],
    'proof': 347913885878,
    'previous_hash': '71fd5ae834fbbdde8fe28f543a00e4bced288685fb78f8482b6296f48a9a720d'
}
```

类似于数据结构中的链表，区块链中的每一个区块包含了可以唯一确认上一个区块的哈希值 `previous_hash`。

通过这个哈希值，区块被链接在一起，所以叫区块链。

这个哈希值是区块链技术的关键点：
区块间用哈希关联，让区块链变成了不可变的数据结构。如果任何一个区块被改变，比如被入侵修改，该区块的哈希值就会变化，
这个区块之后**所有**区块的 `previous_hash` 都变成了错误的哈希值。
