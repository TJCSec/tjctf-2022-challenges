from pwn import remote, args

host = args.HOST or 'localhost'
port = args.PORT or 31996

r = remote(host, port)

r.recvuntil(b'public key (n, g) = (')
n = int(r.recvuntil(b',', drop=True))
r.recvuntil(b'E(4) = ')
e4 = int(r.recvline())
s = n ** 2

# first generate encryptions of powers of 2 starting at 4
encs = [-1, -1, e4]
# encs[i] = ENC(2^i)
for _ in range(n.bit_length()):
    encs.append((encs[-1] * encs[-1]) % s)

def construct(t):
    r = 1
    i = 0
    while t:
        if (t & 1) == 1:
            r = (r * encs[i]) % s
        t >>= 1
        i += 1
    return r

target = int.from_bytes(b"Please give me the flag", "big")

# n is odd so one of these must be true
# alternatively, could write only one exploit and rerun until it works
# (50% chance each time)
if (n + 1) % 4 == 0:
    encs[0] = construct(n + 1)
    encs[1] = (encs[0] * encs[0]) % s
    m = construct(target)
elif (n + 3) % 4 == 0:
    e3 = construct(n + 3)
    # note that target ends in 0b11
    m = (construct(target ^ 0b11) * construct(n + 3)) % s

r.sendline(str(m))
r.stream()
