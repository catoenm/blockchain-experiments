import hashlib
from typing import List

"""
Core Objects
"""


class Transaction:
    def __init__(self, sender: str, receiver: str, value: float):
        self.sender = sender
        self.receiver = receiver
        self.value = value


class MerkleNode:
    def __init__(self, val: str, left: 'MerkleNode', right: 'MerkleNode'):
        self.val = val
        self.left = left
        self.right = right


class MerkleTree:
    def __init__(self, transactions: List[Transaction]):
        merkle_nodes = [MerkleNode(get_transaction_id(
            t), None, None) for t in transactions]
        while(len(merkle_nodes) > 1):
            merkle_nodes = generate_next_merkle_level(merkle_nodes)

        self.root: MerkleNode = merkle_nodes[0]


"""
Merkle Tree Helper Functions
"""


def get_transaction_id(transaction: Transaction):
    return hashlib.sha256(
        f"{transaction.sender}-{transaction.receiver}-{transaction.value}"
        .encode('utf-8'))


def generate_new_hash(h1: str, h2: str):
    return hashlib.sha256(f"{h1}-{h2}".encode("utf-8"))


def generate_next_merkle_level(merkle_nodes: List[MerkleNode]):
    result = []
    # Iterate through hashes, two at a time
    for i in range(0, len(merkle_nodes), 2):
        # If there is an odd number of hashes, copy the final one
        node_pair = [merkle_nodes[i], merkle_nodes[i]]
        if i + 1 < len(merkle_nodes):
            node_pair[1] = merkle_nodes[i+1]
        # Generate the resulting hash
        result.append(MerkleNode(
            generate_new_hash(
                node_pair[0].val.hexdigest(), node_pair[1].val.hexdigest()),
            node_pair[0],
            node_pair[1]))
    return result
