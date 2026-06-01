import pymerkle
from pymerkle import InmemoryTree as MerkleTree

tree = MerkleTree(algorithm='sha256')

index = tree.append_entry(b'foo')   # leaf index

value = tree.get_leaf(index)        # leaf hash

print(f'leaf index: {index}')
print(f'leaf hash: {value.hex()}')