from random import randint
from math import gcd
import math

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

# Modular inverse
def modular_inv(a, b):
    if b==0:
        v = 0
        return v
    else:
        u, d = 1, a
        v1, v3 = 0, b
        while v3 != 0:
            q, t3 = math.floor(d / v3), d % v3
            t1 = u - q * v1
            u = v1
            d = v3
            v1 = t1
            v3 = t3
        v = (d - a * u) / b
        return v
    return None

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

# Step function for Pollard's rho for DLP
def f(xab, g, h, p):
    x, a, b = xab[0], xab[1], xab[2]
    if x%3 == 0:
        return [x*h%p, (a+1)%(p-1), b]
    elif x%3 == 1:
        return [x*x%p, a*2%(p-1), b*2%(p - 1)]
    else:
        return [x*g%p, a, (b+1)%(p-1)]
    return None

# Pollard's rho for DLP
def pollard_rho_dl(g, h, p):
    xab = 1, 0, 0
    XAB = f(xab, g, h, p)
    i = 1
    while xab[0] != XAB[0]:
        i, xab, XAB = i+1, f(xab,g,h,p), f(f(XAB,g,h,p),g,h,p)
    d = gcd(xab[1]-XAB[1], p-1)
    if d == 1: return ((XAB[2]-xab[2])*modular_inv(xab[1]-XAB[1], p-1)) % (p-1)
    m, l = 0, int(((XAB[2]-xab[2])*modular_inv(xab[1]-XAB[1],(p-1)/d))%((p-1)/d))
    while m <= d:
        if modular_pow(g,l,p) == h%p: return l
        m, l = m+1, int((l+((p-1)/d))%(p-1))
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
