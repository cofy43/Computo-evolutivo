import math
import numpy as np

def fix_precision(real,precision):
    s = "{:.{}f}".format(real,precision)
    return float(s)

def real_entero(real,precision):
    return int(real * math.pow(10,precision))

def size_rep_bin(ub,lb,precision):
    return math.floor(math.log2(math.pow(10,precision)*(ub-lb)))+1

def size_rep_bin_vector(ub,lb,precision,nvar):
    size = []
    i = 0
    while i < nvar:
        size.append(size_rep_bin(ub[i],lb[i],precision[i]))
        i += 1
    return size

def rep_binaria(real,ub,lb,precision,size):
    if real > ub:
        return rep_binaria(ub,ub,lb,precision,size)
    if real < lb:
        return [0]*size
    real = real_entero(fix_precision(real,precision),precision)
    u = real_entero(fix_precision(ub,precision),precision)
    bit_a = []
    if real == lb:
        bit_a = [0]*size
    else:
        bit_a = bin_a(str("{:0{}b}").format(u+real,size),size)
    return bit_a
    
def bin_a(n,size):
    i = 0
    bit_a = [0]*size
    for x in list(n):
        if x == '1':
            bit_a[i] = 1
        else:
            bit_a[i] = 0
        i += 1
    return bit_a

def rep_real(bin_a,lb,precision):
    n = len(bin_a)
    num=0
    i=0
    for x in bin_a:
        num += x*math.pow(2,n-i-1)
        i += 1
    return fix_precision(lb + num*(math.pow(10,(-1 * precision))),precision)

def rep_entera(bin_a):
    n = len(bin_a)
    num=0
    i=0
    for x in bin_a:
        num += x*math.pow(2,n-i-1)
        i += 1
    return int(num)


def rep_vector_bin(real,ub,lb,precision,size,nvar):
    bin_a = []
    i = 0
    while i < nvar:
        bin_a += rep_binaria(real[i],ub[i],lb[i],precision[i],size[i])
        i += 1
    return bin_a


def rep_vector_real(bin_a,lb,precision,size,nvar):
    s = 0
    v = []
    i = 0
    while i < nvar:
        f = s + size[i]
        v.append(rep_real(bin_a[s:f],lb[i],precision[i]))
        s = f
        i += 1
    return v
