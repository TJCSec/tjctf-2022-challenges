enc = "fxqftiuuus\x7fw`aaaaaaaaa'ao"
print(''.join([chr(ord(c) ^ 0x12) for c in enc]))
