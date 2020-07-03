from functools import reduce
import numpy as np

def int2bin(x, n):
    '''
    Converts input integer 'x' into an 'n' binary vector
    '''
    bit_str = bin(x)[2:]
    bit_str = '0' * (n - len(bit_str)) + bit_str
    bits = tuple(int(v) for v in bit_str)
    return bits[::-1]

def find_bias(p, q, F):
    '''
    Given polynomial p = q, calculates the number of times it is satisfied by the S-box fn F
    and finds the bias from 1/2.
    '''
    count = 0
    for x, y in enumerate(F):
        lhs, rhs = 0, 0
        lhs = reduce(lambda i, j: int(i) ^ int(j), bin(p & x)[2:])
        rhs = reduce(lambda i, j: int(i) ^ int(j), bin(q & y)[2:])
        if int(lhs) == int(rhs):
            count += 1
    return count / len(F) - 1 / 2

def generate_bias_table(SBOX):
    N = len(SBOX)
    T = np.zeros((N, N))
    for r in range(N):
        for c in range(N):
            bias = find_bias(r, c, SBOX)
            T[r, c] = bias * N
    return T
