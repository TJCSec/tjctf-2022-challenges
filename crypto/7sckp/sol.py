from pwn import remote, args
from Crypto.Cipher import AES
from time import time
import random
from tqdm import trange

BLOCK_SIZE = AES.block_size

host = args.HOST or 'localhost'
port = args.PORT or 31566

io = remote(host, port)
io.recvuntil(b'custom padding!')
seed = int(time() // 10)
random.seed(seed)

p = b''
while len(p) < BLOCK_SIZE:
    b = bytes([random.randrange(256)])
    if b not in p:
        p += b


def check(msg):
    io.recvuntil(b"Ciphertext: ")
    io.sendline(msg.hex())
    line = io.recvline().strip()
    return line == b'ok'


def find_block(token_enc, block_num):
    token_enc = token_enc[block_num*BLOCK_SIZE:]
    padding = b''
    block = b''
    offset = BLOCK_SIZE - 1

    intermediates = []

    for offset in trange(BLOCK_SIZE - 1, -1, -1, desc=f'decrypting block {block_num}'):
        padding = [inter ^ p[i + 1] for i, inter in enumerate(intermediates)]
        for b in range(256):
            payload = (token_enc[:offset] + bytes([b] + padding) + token_enc[BLOCK_SIZE:BLOCK_SIZE*2])
            poss = check(payload)

            if poss:
                intermediate = b ^ p[0]
                intermediates.insert(0, intermediate)
                block = bytes([intermediate ^ token_enc[offset]]) + block
                break
        else:
            raise ValueError('wtmoo')

    return block


io.recvuntil(': ')
token_enc = bytes.fromhex(io.recvline().strip().decode())

flag = b''.join([find_block(token_enc, i) for i in range((len(token_enc) // BLOCK_SIZE) - 1)])
pad_start = flag.rindex(p[0])
flag = flag[:pad_start]
print(flag.decode())
