import math
import numpy as np

def real(bin_a,ub,lb,accuracy):
    i = 0
    num = 0
    for x in bin_a:
        num += x*math.pow(2,accuracy-i-1)
        i += 1
    return ((num / math.pow(2,accuracy)) * (ub - lb)) + lb

def bin_a(accuracy):
    bit_a = []
    for i in range(0,accuracy):
        x = np.random.uniform()
        if x < 0.5:
            bit_a.append(0)
        else:
            bit_a.append(1)
    return bit_a