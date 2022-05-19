import pygraphviz as pgv
from more_itertools import chunked
from crccheck.crc import Crc16

p16 = lambda x: x.to_bytes(2, 'little')
u16 = lambda b: int.from_bytes(b, 'little')
data = open('dump', 'rb').read()
data = [u16(data[i:i+2]) for i in range(0, len(data), 2)]
start = data.pop(0)

def draw_tree():
  G = pgv.AGraph(directed=True)
  def parse(i):
    symbol, freq, left, right = data[i:i+4]
    if left == 0 and right == 0:
      # leaf
      label = f'0x{symbol:02x}'
      G.add_node(label)
      return label
    else:
      # internal
      label = f'{i}'
      G.add_node(label)
      if left != 0:
        G.add_edge(label, parse(left), label='0')
      if right != 0:
        G.add_edge(label, parse(right), label='1')
      return label
  parse(start)
  return G

# G = draw_tree()
# G.layout(prog='dot')
# G.draw('tree.png')

def get_encoding():
  encoding = {}
  def parse(i, path=''):
    symbol, freq, left, right = data[i:i+4]
    if left == 0 and right == 0:
      encoding[symbol] = path
    else:
      parse(left, path + '0')
      parse(right, path + '1')
  parse(start)
  return encoding

flag = open('flag.bin', 'rb').read()
if len(flag) % 2 == 1:
  flag += b'\x00'
crc = Crc16().process(flag).finalbytes()[::-1]

encoding = get_encoding()
bits = ''.join(encoding[x] for x in flag)
encoded = b''
for word in chunked(bits, 16):
  encoded += p16(int(''.join(word[::-1]), 2))
solution = p16(len(flag)) + crc + encoded

with open('solution', 'wb') as f:
  f.write(solution)
