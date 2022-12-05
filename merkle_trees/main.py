import hashlib
import random
from typing import List
from merkle_tree import MerkleTree, Transaction


def generate_public_keys(num_keys: int):
    return [hashlib.sha256(str(i).encode('utf-8')).hexdigest() for i in range(num_keys)]


def generate_transactions(pubkeys: List[str], num_transactions: int):
    transactions = []
    for i in range(num_transactions):
        r1 = random.randint(0, len(pubkeys)-1)
        r2 = random.randint(0, len(pubkeys)-1)
        transactions.append(Transaction(
            pubkeys[r1], pubkeys[r2], random.randint(0, 10000)))
    return transactions


# Create experimental merkle trees
pubkeys = generate_public_keys(100)
transactions: List[Transaction] = generate_transactions(pubkeys, 6)
merkle_tree = MerkleTree(transactions)
identical_merkle_tree = MerkleTree(transactions)

# Mess with the data in a single transaction
transactions[random.randint(0, len(transactions))-1].value += 1
malicious_merkle_tree = MerkleTree(transactions)

# Verify basic merkle tree functionality holds
assert (merkle_tree.root.val.hexdigest() ==
        identical_merkle_tree.root.val.hexdigest())
assert (merkle_tree.root.val.hexdigest() !=
        malicious_merkle_tree.root.val.hexdigest())
