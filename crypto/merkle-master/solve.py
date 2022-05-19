from pwn import remote, args
from tqdm import trange
import hashlib

host = args.HOST or 'localhost'
port = args.PORT or 31979

r = remote(host, port)

class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        s = f"<Node {str(self)}"
        if self.left is not None:
            s += " L"
        if self.right is not None:
            s += " R"
        s += ">"
        return s

    def __str__(self):
        return f"{self.val.hex()[-8:]}"


class MerkleTree:
    def __init__(self, data):
        # not very efficient, fix later
        while (len(data) - 1) & len(data) != 0:
            data.append(b'')
        self.data = data
        self.data_lookup = {v:i for i,v in enumerate(self.data)}
        self._build()

    def _build(self):
        self.leaves = [Node(hashlib.sha256(val).digest()) for val in self.data]
        cur = self.leaves
        while len(cur) > 1:
            new = []
            for i in range(0,len(cur),2):
                left = cur[i]
                right = cur[i+1]
                cat_digest = left.val + right.val
                res_digest = hashlib.sha256(cat_digest).digest()
                new.append(Node(res_digest, left=left, right=right))
                left.parent = new[-1]
                right.parent = new[-1]
            cur = new
        self.root, = cur
        self.commitment = self.root.val

    def _generate_proof_for_idx(self, idx):
        lo = 0
        hi = len(self.data)
        path = []
        cur = self.root
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if idx < mid:
                path.append(("L", cur.right.val))
                cur = cur.left
                hi = mid
            else:
                path.append(("R", cur.left.val))
                cur = cur.right
                lo = mid
        return path

    def generate_membership_proof(self, element):
        if element not in self.data_lookup:
            raise Exception("Element not in data!")
        index = self.data_lookup[element]
        return self._generate_proof_for_idx(index)


def format_proof(proof):
    return str([[a, b.hex()] for a, b in proof]).replace("'", '"')


r.recvuntil(b'care about:\n\n')
req_data = r.recvuntil(b'Commitment hash', drop=True).decode().strip().split('\n')
req_data.sort()

modified_data = []
for d in req_data:
    # these entries are for proving non-existence
    modified_data.append(d[:-1])
    modified_data.append(d + "_")

    # these are for proving existence
    modified_data.append(d)

# => N (50) "bad values"
# want odds of not hitting a bad value to be high
# with 100k elements of padding, get ~60% success chance
# closest power of 2 is 131k  (2^17)

TREE_DEPTH = 17
TARGET_LENGTH = 1 << 17
PADDING_LENGTH = TARGET_LENGTH - len(modified_data)
merkle_data = ["000000000000" for _ in range(PADDING_LENGTH)]
merkle_data.extend(modified_data)
merkle_data = [x.encode() for x in merkle_data]

tree = MerkleTree(merkle_data)
r.sendline(tree.commitment.hex().encode())
r.sendlineafter(b'Tree depth: ', str(TREE_DEPTH).encode())

for _ in trange(50, desc='checking'):
    task = r.recvline()
    data = task[12:24]
    if b"is part of" in task:
        #print("proving existence of",data)
        proof = tree.generate_membership_proof(data)
        r.sendline(format_proof(proof).encode())
    else:
        #print("proving nonexistence of",data)
        left_data = data[:-1]
        right_data = data + b"_"

        r.sendline(left_data)
        left_proof = tree.generate_membership_proof(left_data)
        r.sendline(format_proof(left_proof).encode())

        r.sendline(right_data)
        right_proof = tree.generate_membership_proof(right_data)
        r.sendline(format_proof(right_proof).encode())
    r.recvuntil(b'OK\n\n')

r.recvuntil(b'these indices:\n')
indices = list(map(int, r.recvline().decode().strip().split()))

for index in indices:
    data = tree.data[index]
    r.sendline(data)
    proof = tree._generate_proof_for_idx(index)
    r.sendline(format_proof(proof).encode())

r.recvuntil(b'Master.\n')
r.stream()
