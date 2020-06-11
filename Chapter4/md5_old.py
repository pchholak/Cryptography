import math

M = [1, 0, 1, 1]
b = len(M)

M.append(1)
while (len(M)%512) != 448:
    M.append(0)

W = list(map(int, bin(b)[2:]))
while len(W) < 64:
    W.append(0)
if len(W) > 64:
    print("b > 2^64")
    l = W[-32:]
    h = W[-64:-32]
    W = l + h
M = M + W
N = len(M)
N

A = 0x01234567
B = 0x89abcdef
C = 0xfedcba98
D = 0x76543210

T = [int(4294967296 * abs(math.sin(i))) for i in range(1, 65)]
def F(x, y, z):
    return (x & y) | ((~x) & z)

def G(x, y, z):
    return (x & z) | (y & (~z))

def H(x, y, z):
    return x ^ y ^ z

def I(x, y, z):
    return y ^ (x | (~z))

def round1(a, b, c, d, k, s, i):
    a = (b + ((a + F(b, c, d) + X[k] + T[i]) << s)) % pow(2, 32)
    return a

X = [None] * 16
for i in range(int(N / 16)):
    for j in range(15):
        X[j] = M[i * 16 + j]
    AA, BB, CC, DD = A, B, C, D

    # Round-1
    a = round1(a, b, c, d)
