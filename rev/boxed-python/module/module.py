from numba.pycc import CC
import numpy as np

cc = CC('box')
cc.verbose = True

flag = open('flag.txt', 'rb').read().strip()
x = np.array(list(flag), dtype=np.float64)
A = np.random.randint(100, 1000, (len(flag) - 7, len(flag))).astype(np.float64)
b = A @ x

@cc.export('check', 'b1(f8[:])')
def check(x):
  return np.array_equal(A @ x, b)

@cc.export('size', 'i8()')
def size():
  return len(flag)

if __name__ == '__main__':
  cc.compile()
