def arr_inv(xyz):
    pqr = [None] * len(xyz)
    for i, pos in enumerate(xyz):
        pqr[pos] = i
    return pqr

S = [16, 42, 28, 3, 26, 0, 31, 46, 27, 14, 49, 62, 37, 56, 23, 6, 40,
    48, 53, 8, 20, 25, 33, 1, 2, 63, 15, 34, 55, 21, 39, 57, 54, 45,
    47, 13, 7, 44, 61, 9, 60, 32, 22, 29, 52, 19, 12, 50, 5, 51, 11,
    18, 59, 41, 36, 30, 17, 38, 10, 4, 58, 43, 35, 24]

P = [24, 5, 15, 23, 14, 32, 19, 18, 26, 17, 6, 12, 34, 9, 8, 20, 28, 0,
        2, 21, 29, 11, 33, 22, 30, 31, 1, 25, 3, 35, 16, 13, 27, 7, 10, 4]

S_INV = arr_inv(S)
P_INV = arr_inv(P)

########################################
# S-box function
########################################
def sbox(x):
    return S[x]

########################################
# P-box function
########################################
def pbox(x):
    y = 0
    # For each bit to be shuffled
    for i in range(len(P)):
        # If the original bit position
        # is a 1, then make the result
        # bit position have a 1
        if (x & (1 << i)) != 0:
            y = y ^ (1 << P[i])
    return y

########################################
# S-box inverse function
########################################
def asbox(x):
    return S_INV[x]

########################################
# P-box inverse function
########################################
def apbox(x):
    y = 0
    # For each bit to be shuffled
    for i in range(len(P_INV)):
        # If the original bit position
        # is a 1, then make the result
        # bit position have a 1
        if (x & (1 << i)) != 0:
            y = y ^ (1 << P_INV[i])
    return y

########################################
# Takes 36-bit to six 6-bit values
# and vice-versa
########################################
def demux(x):
    y = []
    for i in range(6):
        y.append((x >> (i * 6)) & 0x3f)

    return y

def mux(x):
    y = 0
    for i in range(6):
        y = y ^ (x[i] << (i * 6))

    return y

########################################
# Key mixing
########################################
def mix(p, k):
    v = []
    key = demux(k)
    for i in range(6):
        v.append(p[i] ^ key[i])

    return v

########################################
# Round function
########################################
def round(p, k):
    u = []

    # Calculate the S-boxes
    for x in demux(p):
        u.append(sbox(x))

    # Run through the P-box
    v = demux(pbox(mux(u)))

    # XOR in the key
    w = mix(v, k)

    # Glue back together, return
    return mux(w)

########################################
# Encryption
########################################
def encrypt(p, rounds, key_secret):
    key_round = generate_round_key(key_secret)
    x = p
    for i in range(rounds):
        x = round(x, key_round)
    return x

########################################
# Opposite of the round function
########################################
def unround(c, k):
    x = demux(c)
    u = mix(x, k)
    v = demux(apbox(mux(u)))
    w = []
    for s in v:
        w.append(asbox(s))

    return mux(w)

########################################
# Decryption function
########################################
def decrypt(c, rounds, key_secret):
    key_round = generate_round_key(key_secret)
    x = c
    for i in range(rounds):
        x = unround(x, key_round)

    return x

########################################
# Copy and concatenate left and right
# key halves
########################################
def generate_round_key(key_secret):
    return (key_secret << 18) ^ key_secret
