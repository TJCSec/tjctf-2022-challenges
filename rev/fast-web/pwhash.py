from hashlib import sha512
from itertools import chain
from more_itertools import chunked

pw = 'a9c1651c5ed00efe9515475b0c6d8fe8f2e9d098137fc68d8efdbfb83ff691d2'
h = sha512(pw.encode()).digest()
h = bytes(chain.from_iterable(c[::-1] for c in chunked(h, 8)))
h = bytes(chain.from_iterable(c[::-1] for c in chunked(h, 2)))
print(h.hex())
