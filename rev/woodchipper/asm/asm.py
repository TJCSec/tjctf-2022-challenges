import sys
import re
import ast

if len(sys.argv) < 2:
  print(f'{sys.argv[0]} input [output]')
  sys.exit()

p16 = lambda x: x.to_bytes(2, 'little')
u16 = lambda s: int.from_bytes(s, 'little')

scall = {
  'S_exit': 0,
  'S_read': 1,
  'S_write': 2,
  'S_open': 3,
  'S_close': 4,
}

mnem = {
  'add': 0x00,
  'clt': 0x01,
  'and': 0x02,
  'mov': 0x03,
  'shl': 0x04,
  'cet': 0x05,
  'mul': 0x08,
  'cgt': 0x09,
  'xor': 0x0a,
  'cal': 0x0b,
  'rol': 0x0c,
  'jpt': 0x0d,
  'sub': 0x10,
  'cle': 0x11,
  'or': 0x12,
  'sys': 0x13,
  'shr': 0x14,
  'jmp': 0x15,
  'div': 0x18,
  'cge': 0x19,
  'not': 0x1a,
  'ret': 0x1b,
  'ror': 0x1c,
  'jpf': 0x1d,
}

labels = {}
output = []

# smh
parse_label = re.compile(r'(l_[a-z0-9_]+):')
parse_operand = r'\[?(?:r\d{1,2}|0x[0-9a-f]+|[0-9]+|l_[a-z0-9_]+|S_[a-z]+)\]?'
parse_inst = re.compile(r'([a-z]{1,3})(?: (' + parse_operand + r')(?:, ?(' + parse_operand + r'))?)?')

def parse_operand(operand):
  # deref, r/i, value
  if operand[0] == '[' and operand[-1] == ']':
    _, t, v = parse_operand(operand[1:-1])
    return 1, t, v
  if operand[0:2] == 'S_':
    return 0, 1, scall[operand]
  if operand[0:2] == 'l_':
    return 0, 1, operand
  if operand[0] == 'r':
    return 0, 0, int(operand[1:])
  return 0, 1, ast.literal_eval(operand)

with open(sys.argv[1], 'r') as f:
  for line in f:
    line = line.strip()
    if line == '' or line[0] == '#' or line[0] == ';': continue
    match = parse_label.fullmatch(line)
    if match is not None:
      l = match.group(1)
      if l in labels:
        raise ValueError(f'duplicate label "{l}"')
      labels[l] = len(output)
      continue
    if line[:5] == '.var ':
      num = ast.literal_eval(line[5:])
      assert isinstance(num, int)
      output.extend([0]*num)
      continue
    if line[:5] == '.str ':
      raw = ast.literal_eval(line[5:])
      if isinstance(raw, str): raw = raw.encode()
      assert isinstance(raw, bytes)
      for i in range(0, len(raw), 2):
        output.append(u16(raw[i:i+2]))
      continue
    if line[:5] == '.num ':
      num = ast.literal_eval(line[5:])
      assert isinstance(num, int)
      output.append(num)
      continue
    if line[:5] == '.ptr ':
      label = line[5:]
      if label[:2] != 'l_':
        raise ValueError(f'invalid pointer "{label}"')
      output.append(label)
      continue
    match = parse_inst.fullmatch(line)
    if match is None:
      raise ValueError(f'invalid instruction "{line}"')
    groups = match.groups()
    if groups[0] not in mnem:
      raise ValueError(f'invalid mnemonic "{groups[0]}"')
    opcode = mnem[groups[0]]
    end = (groups + (None,)).index(None)
    operands = groups[1:end]
    ops = 0
    reg = 0
    imm = []
    for i, operand in enumerate(operands):
      d, t, v = parse_operand(operand)
      ops |= ((d << 1) | t) << (i * 2)
      if t == 0:
        reg |= v << (i * 2)
      else:
        imm.append(v)
    inst = opcode | (len(operands) << 5) | (ops << 7) | (reg << 11)
    output.append(inst)
    output.extend(imm)

for i, c in enumerate(output):
  if isinstance(c, str):
    if c not in labels:
      raise ValueError(f'undefined symbol "{c}"')
    output[i] = labels[c]

if len(sys.argv) < 3:
  fn = sys.argv[1] + '.bin'
else:
  fn = sys.argv[2]

with open(fn, 'wb') as f:
  for c in output:
    f.write(p16(c))
