from random import randint
from math import gcd

# Sieve of Eratosthenes
def primes(n):
    b = [True] * (n + 1)
    ps = []
    for p in range(2, n + 1):
        if b[p]:
            ps.append(p)
            for i in range(p, n + 1, p):
                b[i] = False
    return ps

# Square-and-multiply algorithm for exponentiation
def exponentiate_sam(x, d, n):
    d_bin = list(bin(d)[2:])
    t = len(d_bin) - 1
    r = x
    for i in range(t-1, -1, -1):
        r = (r * r) % n
        if int(d_bin[t-i]) == 1:
            r = (r * x) % n
    return r

# Pollard's p-1
def pollard_pm1(n, limit):
    a = randint(2, n)
    if gcd(a, n) != 1:
        return gcd(a, n)
    else:
        for p in primes(limit):
            pp = p
            while pp < limit:
                a = exponentiate_sam(a, pp, n)
                g = gcd(a-1, n)
                if (g>1) and (g<n):
                    return g
                pp = p * pp
    return False
