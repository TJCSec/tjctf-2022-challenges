from sage.geometry.hyperbolic_space.hyperbolic_isometry import moebius_transform

from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

CC = ComplexField(1000)
uzw = lambda s: tuple(map(CC, s.split(', ')))

with open('output.txt') as f:
  z1, w1 = uzw(next(f))
  z2, w2 = uzw(next(f))
  z3, w3 = uzw(next(f))
  kz = CC(next(f))
  ct = bytes.fromhex(next(f))
a = Matrix([[z1*w1, w1, 1], [z2*w2, w2, 1], [z3*w3, w3, 1]]).determinant()
b = Matrix([[z1*w1, z1, w1], [z2*w2, z2, w2], [z3*w3, z3, w3]]).determinant()
c = Matrix([[z1, w1, 1], [z2, w2, 1], [z3, w3, 1]]).determinant()
d = Matrix([[z1*w1, z1, 1], [z2*w2, z2, 1], [z3*w3, z3, 1]]).determinant()

M = Matrix([[a, b], [c, d]])
kw = moebius_transform(M, kz)

mod = 2^128
key = (kw.real() * mod).round() % mod
iv = (kw.imag() * mod).round() % mod

cipher = AES.new(long_to_bytes(key), AES.MODE_CBC, iv=long_to_bytes(iv))
print(unpad(cipher.decrypt(ct), AES.block_size).decode())
