from uuid import uuid4
from zipfile import ZipFile, ZIP_DEFLATED

flag = open('flag.txt').read()

with ZipFile('chall.zip', 'w') as zf:
  zf.writestr('flag/', flag, ZIP_DEFLATED)
  for _ in range(100):
     zf.writestr(f'flag/flag-{uuid4()}.txt', 'your flag is in another castle', ZIP_DEFLATED)
