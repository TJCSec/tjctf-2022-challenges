from pwn import remote, args

host = args.HOST or 'localhost'
port = args.PORT or 31415

r = remote(host, port)
r.sendline('1')
r.sendline('4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa200a8284bf36e8e4b55b35f427593d849676da0d1555d8360fb5f07fea2')
r.recvuntil('Tag: ')
tag = r.recvline().strip()
r.sendline('2')
r.sendline('4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa202a8284bf36e8e4b55b35f427593d849676da0d1d55d8360fb5f07fea2')
r.sendline(tag)

r.recvuntil('Flag: ')
print(r.recvline().strip().decode())
