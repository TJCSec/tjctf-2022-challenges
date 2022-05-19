from Crypto.Util.number import *

with open("flag.txt") as f:
    flag = f.read().strip()

flag1 = flag[:len(flag)//2]
flag2 = flag[len(flag)//2:]
m1 = int.from_bytes(flag1.encode(), "big")
m2 = int.from_bytes(flag2.encode(), "big")
p = getPrime(70)
q = getPrime(70)
n = p * q
e = 65537
d = pow(e, -1, (p-1)*(q-1))
c1 = pow(m1, e, n)
c2 = pow(m2, e, n)
assert m1 == pow(c1, d, n)
assert m2 == pow(c2, d, n)

with open("problem.txt", "w") as f:
    f.write(f"""==== SECRET RSA MESSAGE ====
n = {n}
e = {e}
c1 = {c1}
c2 = {c2}
""")
