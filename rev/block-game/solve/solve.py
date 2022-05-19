from itertools import islice, product
from tqdm import tqdm

import numpy as np
import cv2

with open('../bin/data.dat', 'rb') as f:
  data = iter(f.read())

def num():
  return int.from_bytes(bytes(islice(data, 4)), 'big')

def byte():
  return next(data)

px = num()
py = num()
pz = byte()
w = num()
h = num()

game = np.zeros((8, h, w), dtype=np.uint8)

for y, x, z in tqdm(product(range(h), range(w), range(0, 8, 2)), total=(h * w * 4)):
  tiles = byte()
  for i in range(2):
    game[z + i, y, x] = tiles & 15
    tiles >>= 4

def hex2bgr(color):
  b = color & 255
  color >>= 8
  g = color & 255
  color >>= 8
  r = color & 255
  return b, g, r

colors = [
  0x888c8d,
  0xcd8032,
  0xdbb17a,
  0xb37a4c,
  0x009a17,
  0xca9c67,
  0xcfcfcf,
  0xfccd12,
  0x00b2ff,
  0xb9f2ff,
  0x3aab58,
  0x337cba,
  0xf83a0c,
  0x000000,
  0xffffff,
  0x99eaff,
]

lut = np.zeros((256, 1, 3), dtype=np.uint8)
for i, c in enumerate(colors):
  lut[i, 0] = hex2bgr(c)

def cvt_level(level):
  img = cv2.cvtColor(level, cv2.COLOR_GRAY2BGR)
  img = cv2.LUT(img, lut)
  return img

# for i, level in enumerate(game):
#   img = cvt_level(level)
#   cv2.imwrite(f'level_{i}.png', img)

solve = game[0, py-25:py, px-50:px+55]
img = cvt_level(solve)
h, w, _ = img.shape
img = cv2.resize(img, (10 * w, 10 * h), interpolation=cv2.INTER_NEAREST)
cv2.imwrite('solve.png', img)
