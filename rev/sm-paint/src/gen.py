from functools import reduce
from PIL import Image
from random import randrange

im = Image.open('likemeowsmile.png')

w, h = im.size

px = list(im.getdata())


def xor(x, y): return x ^ y


grid_size = 2

data0 = []
data1 = []
data2 = []
data3 = []
for y in range(0, h, grid_size):
    yy = y
    for x in range((y // grid_size) % grid_size, w, grid_size):
        yy += 1
        if yy % grid_size == 0:
            yy -= grid_size

        if yy >= h:
            continue
        data0.append(randrange(0, 256))
        data1.append(data0[-1] ^ px[yy * w + x][0])
        data2.append(data0[-1] ^ px[yy * w + x][1])
        data3.append(sum(px[yy * w + x]) - 255)

data4 = []


def convert_to_uint32(pixel):
    pixel = pixel[:3][::-1] + (pixel[3],)
    return sum([pixel[i] << (i * 8) for i in range(4)])


strip_size = 3
for y in range(h - strip_size + 1):
    for x in range(w):
        data4.append(
            reduce(xor, [convert_to_uint32(px[yy * w + x])
                   for yy in range(y, y + strip_size)])
        )

out = f'''
#include <emscripten.h>

const Uint8 data0[] = {{{ ', '.join([str(x) for x in data0]) }}};

const Uint8 data1[] = {{{ ', '.join([str(x) for x in data1]) }}};

const Uint8 data2[] = {{{ ', '.join([str(x) for x in data2]) }}};

const Uint32 data3[] = {{{ ', '.join([str(x) for x in data3]) }}};

const Uint32 data4[] = {{{ ', '.join([str(x) for x in data4]) }}};
'''

out += '''
Uint32 checkStrip(Uint8 *pixels, int x, int y, int width)
{
    Uint32 *p = (Uint32 *) pixels;
    Uint32 r = 0;
    for (int yy = y; yy < y + strip_size; yy++)
    {
        r ^= p[yy * width + x];
    }

    return r;
}
'''

out += '''
bool checkFlag(Uint8 *pixels, int width, int height)
{
    int i = 0;
    for (int y = 0; y < height; y += grid_size)
    {
        int yy = y;
        for (int x = (y / grid_size) % grid_size; x < width; x += grid_size)
        {
            yy++;
            if (yy % grid_size == 0)
                yy -= grid_size;
            if (yy >= height)
                continue;

            Uint8 r = pixels[4 * (yy * width + x) + 2];
            Uint8 g = pixels[4 * (yy * width + x) + 1];
            Uint8 b = pixels[4 * (yy * width + x) + 0];
            if ((r ^ data0[i]) != data1[i] ||
                (g ^ data0[i]) != data2[i] ||
                (Uint32) r + (Uint32) g + (Uint32) b != data3[i])
                return false;

            i++;
        }
    }

    i = 0;
    for (int y = 0; y < height - strip_size + 1; y++)
    {
        for (int x = 0; x < width; x++)
        {
            if (checkStrip(pixels, x, y, width) != data4[i])
                return false;
            i++;
        }
    }

    return true;
}'''

out = out.replace('grid_size', str(grid_size))
out = out.replace('strip_size', str(strip_size))

# print(f'{data0 = }')
# print(f'{data1 = }')
# print(f'{data2 = }')
# print(f'{data3 = }')
# print(f'{data4 = }')

with open('out.cpp', 'w') as f:
    f.write(out.strip())
