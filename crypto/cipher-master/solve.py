from cipher import *

## TOOLS / HELPER METHODS

def xor_bits(n):
    r = 0
    while n:
        r ^= 1
        n &= n - 1
    return r

def hw(n):
    c = 0
    while n:
        c += 1
        n &= n - 1
    return c

def bn(n):
    return bin(64+n)[3:]

def compute_approx_entry(sbox, input_mask, output_mask, verbose=False):
    count = 0
    for x in range(1<<6):
        y = sbox[x]
        result = xor_bits(x & input_mask) ^ xor_bits(y & output_mask)
        if result == 0:
            if verbose:
                print("+",x,y)
            count += 1
        else:
            if verbose:
                print("-",x,y)
            count -= 1
    return count // 2

cae = compute_approx_entry

def compute_approx_table(sbox):
    table = {}
    for input_mask in range(1<<6):
        for output_mask in range(1<<6):
            table[input_mask, output_mask] = compute_approx_entry(sbox, input_mask, output_mask)
    return table

def get_largest_bias1(table, input_mask):
    best_out = 0
    best_bias = table[input_mask, 0]
    for out in range(1,1<<6):
        bias = table[input_mask, out]
        if abs(bias) > abs(best_bias) or \
           (abs(bias) == abs(best_bias) and hw(out) < hw(best_out)):
            best_out = out
            best_bias = bias
    return best_out, best_bias

def get_largest_bias2(table, output_mask):
    best_in = 0
    best_bias = table[0, output_mask]
    for inm in range(1,1<<6):
        bias = table[inm, output_mask]
        if abs(bias) > abs(best_bias) or \
           (abs(bias) == abs(best_bias) and hw(inm) < hw(best_in)):
            best_in = inm
            best_bias = bias
    return best_in, best_bias

def p(x):
    return 47-pbox[47-x]

def pi(y):
    for x in range(48):
        if p(x) == y:
            return x

ro = lambda x,y : list(range(x,y+1))

def c(*ns):
    r = "".join("1" if i in ns else "0" for i in range(48))
    print(" ".join(r[i:i+6] for i in range(0,48,6)))

def pileup(*biases):
    r = 2**(len(biases)-1)
    for b in biases:
        r *= b/64
    return r

def subsets(items):
    m = len(items)
    for mask in range(1<<m):
        yield [a for i,a in enumerate(items) if (mask>>i)&1]

def bits_to_boxes(bits):
    bits = "".join("1" if b in bits else "0" for b in range(48))
    return to_blocks(int.to_bytes(int(bits,2),6,"big"))

def boxes_to_bits(boxes):
    r = 0
    for b in boxes:
        r <<= 6
        r |= b
    r = bin((1<<48) + r)[3:]
    return [i for i in range(48) if r[i] == "1"]

table1 = compute_approx_table(sbox1)
table2 = compute_approx_table(sbox2)
table3 = compute_approx_table(sbox3)
table4 = compute_approx_table(sbox4)

isbox1 = invert_box(sbox1)
isbox2 = invert_box(sbox2)
isbox3 = invert_box(sbox3)
isbox4 = invert_box(sbox4)

def auto_analyze(f_bits, verbose=False):
    tables = [table1,table2,table3,table4]
    biases = []

    if verbose:
        print(", ".join(f"F{b}" for b in f_bits))
    
    f_boxes = bits_to_boxes(f_bits)
    e_boxes = []
    for i,box in enumerate(f_boxes):
        if box != 0:
            best_prev, best_bias = get_largest_bias2(tables[i%4], box)
            biases.append(best_bias)
            e_boxes.append(best_prev)
        else:
            e_boxes.append(0)
    e_bits = boxes_to_bits(e_boxes)

    if verbose:
        print(", ".join(f"E{b}" for b in e_bits))

    d_bits = [pi(eb) for eb in e_bits]

    if verbose:
        print(", ".join(f"D{b}" for b in d_bits))

    d_boxes = bits_to_boxes(d_bits)
    c_boxes = []
    for i,box in enumerate(d_boxes):
        if box != 0:
            best_prev, best_bias = get_largest_bias2(tables[i%4], box)
            biases.append(best_bias)
            c_boxes.append(best_prev)
        else:
            c_boxes.append(0)
    c_bits = boxes_to_bits(c_boxes)

    if verbose:
        print(", ".join(f"C{b}" for b in c_bits))

    b_bits = [pi(cb) for cb in c_bits]

    if verbose:
        print(", ".join(f"B{b}" for b in b_bits))

    b_boxes = bits_to_boxes(b_bits)
    a_boxes = []
    for i,box in enumerate(b_boxes):
        if box != 0:
            best_prev, best_bias = get_largest_bias2(tables[i%4], box)
            biases.append(best_bias)
            a_boxes.append(best_prev)
        else:
            a_boxes.append(0)

    a_bits = boxes_to_bits(a_boxes)

    if verbose:
        print(", ".join(f"A{b}" for b in a_bits))

    return a_bits, biases



def auto_analyze2(d_bits, verbose=False):
    tables = [table1,table2,table3,table4]
    biases = []

    if verbose:
        print(", ".join(f"D{b}" for b in d_bits))

    d_boxes = bits_to_boxes(d_bits)
    c_boxes = []
    for i,box in enumerate(d_boxes):
        if box != 0:
            best_prev, best_bias = get_largest_bias2(tables[i%4], box)
            biases.append(best_bias)
            c_boxes.append(best_prev)
        else:
            c_boxes.append(0)
    c_bits = boxes_to_bits(c_boxes)

    if verbose:
        print(", ".join(f"C{b}" for b in c_bits))

    b_bits = [pi(cb) for cb in c_bits]

    if verbose:
        print(", ".join(f"B{b}" for b in b_bits))

    b_boxes = bits_to_boxes(b_bits)
    a_boxes = []
    for i,box in enumerate(b_boxes):
        if box != 0:
            best_prev, best_bias = get_largest_bias2(tables[i%4], box)
            biases.append(best_bias)
            a_boxes.append(best_prev)
        else:
            a_boxes.append(0)

    a_bits = boxes_to_bits(a_boxes)

    if verbose:
        print(", ".join(f"A{b}" for b in a_bits))

    return a_bits, biases


## KEY RECOVERY

# placeholder key
cipher = LNRCipher(12 * b"\x00")

with open("flag.txt.enc", "rb") as f:
    flag_enc = f.read()

with open("lol.bmp", "rb") as f:
    image_pt = f.read()

with open("lol.bmp.enc", "rb") as f:
    image_enc = f.read()

known_pairs = []
msg = cipher.pad_message(image_pt)
enc = image_enc

class bitarr:
    def __init__(self, x):
        self.x = int.from_bytes(x, "big")

    def __getitem__(self, i):
        return (self.x >> (47 - i)) & 1


run_extraction = True

if run_extraction:
    import time
    
    print("extracting known pairs...")
    for i in range(0, len(msg), 6):
        pt = xorb(msg[i:i+6], enc[i:i+6])
        ct = enc[i+6:i+12]
        g = [0 for _ in range(8)]
        f2 = [0 for _ in range(8)] # strictly speaking, this isn't f, since this
                             # is the version where we mix k4p before permuting
        e = [0 for _ in range(8)]
        known_pairs.append((bitarr(pt), pt, ct, to_blocks(ct), g, f2, e))

    def crack_k5_block(k5_block_n, a_bits, g_bits):
        print(f"cracking block {k5_block_n} of K5...")
        isbox_n = [isbox1, isbox2, isbox3, isbox4][k5_block_n % 4]
        hits = [0 for _ in range(64)]
        for posskey in range(64):
            if (posskey + 1) % 8 == 0:
                print(f"{posskey+1}/64")
            for a, pt, ct, ctb, g, _, _ in known_pairs:
                h_block_n = ctb[k5_block_n] ^ posskey
                g_block_n = isbox_n[h_block_n]
                r = 0
                for ab in a_bits:
                    r ^= a[ab]
                for gb in g_bits:
                    bn = gb//6
                    v = g_block_n if bn == k5_block_n else g[bn]
                    r ^= (v >> (5 - (gb % 6))) & 1
                if r == 0:
                    hits[posskey] += 1
        biases = [(hit_count / len(known_pairs)) - 0.5 for hit_count in hits]
        top_biases = sorted(list(range(64)), key=lambda posskey : abs(biases[posskey]), reverse=True)
        print("top 5 biases:")
        for idx in top_biases[:5]:
            print(f"{idx:2d} {abs(biases[idx]):.4f}")
        k5_block_r = top_biases[0]
        print(f"deducing K5 block {k5_block_n} as", k5_block_r)
        return k5_block_r

    def crack_k4p_block(k4p_block_n, a_bits, e_bits, USE_ONLY=None):
        print(f"cracking block {k4p_block_n} of K4p...")
        if USE_ONLY is None:
            USE_ONLY = len(known_pairs)
        isbox_n = [isbox1, isbox2, isbox3, isbox4][k4p_block_n % 4]
        hits = [0 for _ in range(64)]
        for posskey in range(64):
            if (posskey + 1) % 8 == 0:
                print(f"{posskey+1}/64")
            for a, pt, ct, ctb, g, f2, e in known_pairs[:USE_ONLY]:
                f_block_n = f2[k4p_block_n] ^ posskey
                e_block_n = isbox_n[f_block_n]
                r = 0
                for ab in a_bits:
                    r ^= a[ab]
                for eb in e_bits:
                    bn = eb//6
                    v = e_block_n if bn == k4p_block_n else e[bn]
                    r ^= (v >> (5 - (eb % 6))) & 1
                if r == 0:
                    hits[posskey] += 1
        biases = [(hit_count / USE_ONLY) - 0.5 for hit_count in hits]
        top_biases = sorted(list(range(64)), key=lambda posskey : abs(biases[posskey]), reverse=True)
        print("top 5 biases:")
        for idx in top_biases[:5]:
            print(f"{idx:2d} {abs(biases[idx]):.4f}")
        k4p_block_r = top_biases[0]
        print(f"deducing K4 block {k4p_block_n} as", k4p_block_r)
        return k4p_block_r
        

    def populate_g_values(k5_block_n, partial_key):
        isbox_n = [isbox1, isbox2, isbox3, isbox4][k5_block_n % 4]
        for a, pt, ct, ctb, g, _, _ in known_pairs:
            h_block_n = ctb[k5_block_n] ^ partial_key
            g_block_n = isbox_n[h_block_n]
            g[k5_block_n] = g_block_n

    def populate_e_values(k4p_block_n, partial_key):
        isbox_n = [isbox1, isbox2, isbox3, isbox4][k4p_block_n % 4]
        for a, pt, ct, ctb, g, f2, e in known_pairs:
            f_block_n = f2[k4p_block_n] ^ partial_key
            e_block_n = isbox_n[f_block_n]
            e[k4p_block_n] = e_block_n

    def populate_f2_values(k5):
        ipbox = invert_box(pbox)
        for a, pt, ct, ctb, g, f2, _ in known_pairs:
            f2c = permute(g, ipbox)
            for i in range(8):
                f2[i] = f2c[i]

# uses key values from a previous run; these are slow, so was just using this
# for testing purposes when working on cracking k4
##    use_saved = True
##    if use_saved:
##        k5_block_2 = 33
##        populate_g_values(2, k5_block_2)
##        k5_block_1 = 51
##        populate_g_values(1, k5_block_1)
##        k5_block_6 = 1
##        populate_g_values(6, k5_block_6)
##        k5_block_0 = 24
##        populate_g_values(0, k5_block_0)
##        k5_block_3 = 59
##        populate_g_values(3, k5_block_3)
##        k5_block_4 = 49
##        populate_g_values(4, k5_block_4)
##        k5_block_7 = 33
##        populate_g_values(7, k5_block_7)
##        k5_block_5 = 37
##        populate_g_values(5, k5_block_5)

    k5_block_2 = crack_k5_block(2, [0, 18, 14, 15], [14])
    populate_g_values(2, k5_block_2)

    k5_block_1 = crack_k5_block(1, [0, 1, 2, 3, 5, 14, 16, 17, 30, 34, 35], [8, 16])
    populate_g_values(1, k5_block_1)

    k5_block_6 = crack_k5_block(6, [14, 16, 24, 26, 27, 46], [6, 12, 36])
    populate_g_values(6, k5_block_6)

    k5_block_0 = crack_k5_block(0, [0, 1, 2, 3, 5, 13, 16], [2, 14, 38])
    populate_g_values(0, k5_block_0)

    k5_block_3 = crack_k5_block(3, [14, 15, 18], [19, 2, 14, 38])
    populate_g_values(3, k5_block_3)

    k5_block_4 = crack_k5_block(4, [0, 1, 2, 3, 5], [28, 16, 20])
    populate_g_values(4, k5_block_4)

    k5_block_7 = crack_k5_block(7, [0, 38, 39], [46, 10, 29])
    populate_g_values(7, k5_block_7)

    k5_block_5 = crack_k5_block(5, [0, 1, 2, 3, 5], [32, 8, 28])
    populate_g_values(5, k5_block_5)

    k5 = [k5_block_0, k5_block_1, k5_block_2, k5_block_3,
          k5_block_4,k5_block_5, k5_block_6, k5_block_7]

    print("[!] RECOVERED K5 AS",k5)

    # due to how the subkeys are used, next what we recover is not k4 directly,
    # but instead the inverse permutation applied to k4

    # also, since we have to go through 1 fewer round, many of the linear
    # characteristics here have larger biases, which is why we operate on only
    # a subset of the known pairs (for speed reasons)

    # some of the k5 characteristics were strong enough for this too, but it
    # isn't worth tuning most of them to make the script faster

    print("populating f2 values...")
    populate_f2_values(k5)

    # all these biases are in the range [0.10, 0.25], so we'd probably be fine
    # with even less known pairs, but this is already very fast
    
    # bias ~0.16
    k4p_block_2 = crack_k4p_block(2, [14, 15, 18], [14], USE_ONLY=100_000)
    populate_e_values(2, k4p_block_2)

    # bias ~0.16
    k4p_block_5 = crack_k4p_block(5, [38, 39], [31], USE_ONLY=100_000)
    populate_e_values(5, k4p_block_5)

    # bias ~0.10
    k4p_block_4 = crack_k4p_block(4, [38, 39], [27, 31], USE_ONLY=100_000)
    populate_e_values(4, k4p_block_4)

    # bias ~0.21
    k4p_block_7 = crack_k4p_block(7, [36, 37], [46, 29], USE_ONLY=100_000)
    populate_e_values(7, k4p_block_7)

    # bias ~0.13
    k4p_block_6 = crack_k4p_block(6, [38, 39], [39, 15, 43], USE_ONLY=100_000)
    populate_e_values(6, k4p_block_6)

    # bias ~0.11
    k4p_block_0 = crack_k4p_block(0, [24, 26], [2, 14, 38], USE_ONLY=100_000)
    populate_e_values(0, k4p_block_0)

    # bias ~0.24
    k4p_block_3 = crack_k4p_block(3, [14, 15], [19, 2, 14, 38], USE_ONLY=100_000)
    populate_e_values(3, k4p_block_3)

    # bias ~0.14
    k4p_block_1 = crack_k4p_block(1, [14, 16, 17], [10, 22, 29, 46], USE_ONLY=100_000)
    populate_e_values(1, k4p_block_1)
    
    k4p = [k4p_block_0, k4p_block_1, k4p_block_2, k4p_block_3,
           k4p_block_4, k4p_block_5, k4p_block_6, k4p_block_7]

    print("[!] RECOVERED K4P AS",k4p)

    k4 = permute(k4p, pbox)

    print("[!] RECOVERED K4 AS", k4)

    # now just reverse the key expansion to get the other round keys
    k3 = xor(k5, subs(rotate(k4), sbox1))
    k2 = xor(k4, k3)
    k1 = xor(k3, subs(rotate(k2), sbox1))
    key = from_blocks(k1) + from_blocks(k2)

    print("[!] RECOVERED MASTER KEY AS", key.hex())

    cipher = LNRCipher(key)

    with open("flag.txt.enc", "rb") as f:
        print(cipher.unpad_message(cipher.decrypt_cbc(f.read())))
    


## logic for finding the linear characteristics to use above

# for the K5 recovery
if False:
    known_g = ro(0,29) + ro(36,47)
    known_f = sorted([pi(x) for x in known_g])
    grouped = [[] for _ in range(8)]
    for y in known_f:
        grouped[y//6].append(y)

    best = 0
    for new_val in range(48):
        if new_val in known_f:
            continue
        for usable in subsets(grouped[new_val//6]):
            _, biases = auto_analyze([new_val] + usable)
            total = pileup(*biases)
            if abs(total) > best:
                best = abs(total)
                print()
                print("new best:",best)
                print("block:", p(new_val)//6)
                print("f values:", [new_val] + usable)
                print("g values:", [p(y) for y in (new_val,*usable)])
                print("a values:", auto_analyze([new_val] + usable)[0])

# for the K4 recovery
if False:
    import math

    known_blocks = [1, 0, 1, 1, 1, 1, 1, 1]
    known_e = sum((known_blocks[i] * ro(6*i,6*i+5) for i in range(8)), start=[])

    known_d = sorted([pi(x) for x in known_e])
    grouped = [[] for _ in range(8)]
    for y in known_d:
        grouped[y//6].append(y)

    best = 0
    for new_val in range(48):
        if new_val in known_d:
            continue
        for usable in subsets(grouped[new_val//6]):
            _, biases = auto_analyze2([new_val] + usable)
            total = pileup(*biases)
            if abs(total) > best:
                best = abs(total)
                print()
                print("new best:",best)
                print("block:", p(new_val)//6)
                print("d values:", [new_val] + usable)
                print("e values:", [p(y) for y in (new_val,*usable)])
                print("a values:", auto_analyze2([new_val] + usable)[0])
