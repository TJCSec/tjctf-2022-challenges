#!/usr/local/bin/python3.10 -u

import random
import signal

import networkx as nx

flag = open('flag.txt').read().strip()
NUM_TESTS = 50
TIMEOUT = 3

banner = f'''
Thank you for helping Andrew find the Costco location with the cheapest cookies!
However, he wants it fast! So now he needs your help finding the shortest route there.
Andrew starts at location 0 and the Costco is located at location 20.
The next 40 lines will contain route information, where each line will be formatted as:
x y z
Where x and y are the location numbers, and z is the distance of that road.
Note: All routes are 2-way roads, so you may go from x to y and from y to x.
Please output the distance of the shortest path there. If there is no possible path, print -1.
You will need to output the correct answer {NUM_TESTS} times to obtain the flag.
'''.strip()

def timeout(*args):
  print('Time\'s up! Be faster next time!')
  raise SystemExit
signal.signal(signal.SIGALRM, timeout)

def inputtimeout(prompt='', t=30):
  signal.alarm(t)
  rv = input(prompt)
  signal.alarm(0)
  return rv

def generate_graph():
  G = nx.Graph()
  for i in range(21):
    G.add_node(i)
  for _ in range(40):
    while True:
      u = random.randrange(21)
      v = random.randrange(21)
      if u != v and not G.has_edge(u, v): break
    d = random.randrange(1, 21)
    G.add_edge(u, v, weight=d)
  return G

def do_test(test_num):
  G = generate_graph()
  try:
    correct = nx.shortest_path_length(G, source=0, target=20, weight='weight')
  except nx.NetworkXNoPath:
    correct = -1
  print('Here are the routes:')
  for edge in G.edges.data('weight'):
    print(*edge)
  print(f'Andrew wants your answer in {TIMEOUT} seconds, starting now. Hurry up!')
  try:
    ans = int(inputtimeout('Enter your answer: ', TIMEOUT))
  except ValueError:
    print('Sorry! That\'s not a number!')
    raise SystemExit

  if ans != correct:
    print('Sorry! That\'s incorrect!')
    raise SystemExit

  print(f'Test {test_num + 1} passed!')

def main():
  print(banner)
  for test_num in range(NUM_TESTS):
    do_test(test_num)
  print(flag)

if __name__ == '__main__': main()
