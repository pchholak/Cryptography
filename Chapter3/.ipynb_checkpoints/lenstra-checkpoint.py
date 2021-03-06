{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "from random import randint\n",
    "from math import gcd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Sieve of Eratosthenes\n",
    "def primes(n):\n",
    "    b = [True] * (n + 1)\n",
    "    ps = []\n",
    "    for p in range(2, n + 1):\n",
    "        if b[p]:\n",
    "            ps.append(p)\n",
    "            for i in range(p, n + 1, p):\n",
    "                b[i] = False\n",
    "    return ps\n",
    "\n",
    "# Finds modular inverse\n",
    "# Returns inverse, unused helper and gcd\n",
    "def modular_inv(a, b):\n",
    "    if b == 0:\n",
    "        return 1, 0, a\n",
    "    q, r = divmod(a, b)\n",
    "    x, y, g = modular_inv(b, r)\n",
    "    return y, x - q * y, g\n",
    "\n",
    "# Addition in Elliptic curve modulo m space\n",
    "def elliptic_add(p, q, a, b, m):\n",
    "    # if one point is infinity, return the other one\n",
    "    if p[2] == 0: return q\n",
    "    if q[2] == 0: return p\n",
    "    if p[0] == q[0]:\n",
    "        if (p[1] + q[1]) % m == 0:\n",
    "            return 0, 1, 0 # infinity\n",
    "        num = (3 * p[0] * p[0] + a) % m\n",
    "        denom = (2 * p[1]) % m\n",
    "    else:\n",
    "        num = (q[1] - p[1]) % m\n",
    "        denom = (q[0] - p[0]) % m\n",
    "    inv, _, g = modular_inv(denom, m)\n",
    "    # Unable to find inverse, arithmetic breaks\n",
    "    if g > 1:\n",
    "        return 0, 0, denom # Failure\n",
    "    z = (num * inv * num * inv - p[0] - q[0]) % m\n",
    "    return z, (num * inv * (p[0] - z) - p[1]) % m, 1\n",
    "\n",
    "# Multiplication (repeated addition and doubling)\n",
    "def elliptic_mul(k, p, a, b, m):\n",
    "    r = (0, 1, 0) # Infinity\n",
    "    while k > 0:\n",
    "        # p is failure, return it\n",
    "        if p[2] > 1:\n",
    "            return p\n",
    "        if k % 2 == 1:\n",
    "            r = elliptic_add(p, r, a, b, m)\n",
    "        k = k // 2\n",
    "        p = elliptic_add(p, p, a, b, m)\n",
    "    return r\n",
    "\n",
    "# Lenstra's algorithm for factoring\n",
    "# Limit specifies the amount of work permitted\n",
    "def lenstra(n, limit):\n",
    "    g = n\n",
    "    while g == n:\n",
    "        # Randomized x and y\n",
    "        q = randint(0, n - 1), randint(0, n - 1), 1\n",
    "        # Randomized curve coefficient a, computed b\n",
    "        a = randint(0, n - 1)\n",
    "        b = (q[1] * q[1] - q[0] * q[0] * q[0] - a * q[0]) % n\n",
    "        g = gcd(4 * a * a * a + 27 * b * b, n) # singularity check\n",
    "    # if we got lucky, return lucky factor\n",
    "    if g > 1:\n",
    "        return g\n",
    "    # increase k step by step until lcm(1, ..., limit)\n",
    "    for p in primes(limit):\n",
    "        pp = p\n",
    "        while pp < limit:\n",
    "            q = elliptic_mul(p, q, a, b, n)\n",
    "            # Elliptic arithmetic breaks\n",
    "            if q[2] > 1:\n",
    "                return gcd(q[2], n)\n",
    "            pp = p * pp\n",
    "    return False"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "4"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "lenstra(100, 10)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
