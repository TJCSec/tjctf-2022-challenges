with open("problem.txt") as f:
    s = f.read().strip().split("\n")[1:]
n,e,c1,c2 = [int(x[4:].strip()) for x in s]
(p,_),(q,_) = factor(n)
d = int(pow(e, -1, (p-1)*(q-1)))
m1 = pow(c1, d, n)
m2 = pow(c2, d, n)
flag1 = m1.to_bytes((m1.bit_length()+7)//8, "big")
flag2 = m2.to_bytes((m2.bit_length()+7)//8, "big")
print((flag1 + flag2).decode())
