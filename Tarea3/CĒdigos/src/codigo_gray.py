

def xor(p,q):
    if p == 1 and q == 1:
        return 0
    elif p == 0 and q == 0:
        return 0
    else:
        return 1

def neg(p):
    if p == 1:
        return 0
    return 1


def bin_Gray(bit_a):
    g = []
    g.append(bit_a[0])
    i = 1
    while i < len(bit_a):
        g.append(xor(bit_a[i-1],bit_a[i]))
        i += 1
    return g

def Gray_bin(bit_a):
    b = []
    v = bit_a[0]
    b.append(v)
    i = 1
    while i < len(bit_a):
        if bit_a[i] == 1:
            v = neg(v)
        b.append(v)
        i += 1
    return b