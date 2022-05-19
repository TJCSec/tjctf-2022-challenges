from pwn import remote, args
import networkx as nx

host = args.HOST or 'localhost'
port = args.PORT or 31111

r = remote(host, port)
r.recvuntil(b'correct answer ')
num_tests = int(r.recvuntil(b' '))

for _ in range(num_tests):
	G = nx.Graph()
	for i in range(21):
		G.add_node(i)
	r.recvuntil(b'routes:\n')
	for __ in range(40):
		u, v, d = map(int, r.recvline().strip().split())
		G.add_edge(u, v, weight=d)
	try:
		correct = nx.shortest_path_length(G, source=0, target=20, weight='weight')
	except nx.NetworkXNoPath:
		correct = -1
	r.sendline(str(correct).encode())

r.recvuntil(f'Test {num_tests} passed!\n'.encode())
print(r.recvline().strip().decode())
