import numpy as np
import box

def main():
  try:
    inp = input('What\'s the flag? ').encode()
    inp = np.array(list(inp), dtype=np.float64)
    if inp.size != box.size():
      print('Not even close!')
      raise SystemExit
    if not box.check(inp):
      print('Nope!')
      raise SystemExit
    print('hmm... that might be the flag...')
  except:
    pass

if __name__ == '__main__': main()
