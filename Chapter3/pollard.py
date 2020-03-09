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
def modular_pow(x, d, n):
    d_bin = list(bin(d)[2:])
    t = len(d_bin) - 1
    r = x
    for i in range(t-1, -1, -1):
        r = (r * r) % n
        if int(d_bin[t-i]) == 1:
            r = (r * x) % n
    return r

# Modular square function for pollard's rho calculations
def modular_sqr(x, n):
    f = (x * x) % n
    return f

# Pollard's rho algorithm for factorization
def pollard_rho(n):
    x, c = randint(0, n), randint(1, n-2)
    y = x
    g = 1
    while g == 1:
        # Tortoise
        x = modular_sqr(x, n)
        # Hare
        y = modular_sqr(y, n)
        y = modular_sqr(y, n)
        # Check gcd
        g = gcd(abs(x-y), n)
    if g == n:
        return pollard_rho(n)
    else:
        return g
    return None

# Pollard's p-1
def pollard_pm1(n, limit):
    a = randint(2, n)
    if gcd(a, n) != 1:
        return gcd(a, n)
    else:
        for p in primes(limit):
            pp = p
            while pp < limit:
                a = modular_pow(a, pp, n)
                g = gcd(a-1, n)
                if (g>1) and (g<n):
                    return g
                pp = p * pp
    return False
