import math
from math import gcd
from random import randint

def get_primes(n):
    b = [True] * (n + 1)
    ps = []
    for p in range(2, n + 1):
        if b[p]:
            ps.append(p)
            for i in range(p, n + 1, p):
                b[i] = False
    return ps

def exponentiate_sam(x, d, n):
    d_bin = list(bin(d)[2:])
    t = len(d_bin) - 1
    r = x
    for i in range(t-1, -1, -1):
        r = (r * r) % n
        if int(d_bin[t-i]) == 1:
            r = (r * x) % n
    return r

def pollard_pm1(a, B):
    b = 2
    primes = get_primes(B ** 2)
    for i, pi in enumerate(primes):
        e = math.floor(math.log(B, 10) / math.log(pi, 10))
        f = pi ** e
        b = exponentiate_sam(b, f, a)
    g = gcd(b - 1, a)
    if (g>1) and (g<a):
        return g
    else:
        print("Method failed!")
        return None
    return None

def pollard_pm1_charest(n, B):
    primes = get_primes(B ** 2)
    m = 1
    for i, p in enumerate(primes):
        exp = math.floor(math.log(B, 10) / math.log(p, 10))
        m = m * (p ** exp)
    a = randint(1, n)
    d = gcd(a, n)
    e = None
    while True:
        if d==1:
            print("d = 1")
            w = exponentiate_sam(a, m, n)
            e = gcd(w - 1, n)
            if (e!=1) and (e!=n):
                return e
            elif e==n:
                print("e = n; repeating with new random values of 'a'")
                a = randint(1, n)
                d = gcd(a, n)
            else:
                print("Method failed. Increase B!")
                e = None
                break
        else:
            return d
    return e
