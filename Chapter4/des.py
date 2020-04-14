import struct
from enum import Enum
from bitarray import bitarray

class DES_nums(Enum):
    L = 0
    R = 0
    C = 0
    D = 0

class DES_tables(Enum):
    # Initial permutation
    IP =     [58, 50, 42, 34, 26, 18, 10, 2,
              60, 52, 44, 36, 28, 20, 12, 4,
              62, 54, 46, 38, 30, 22, 14, 6,
              64, 56, 48, 40, 32, 24, 16, 8,
              57, 49, 41, 33, 25, 17, 9,  1,
              59, 51, 43, 35, 27, 19, 11, 3,
              61, 53, 45, 37, 29, 21, 13, 5,
              63, 55, 47, 39, 31, 23, 15, 7]

    # Final permutation
    IP_inv = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9,  49, 17, 57, 25]

    # Expansion box for the data
    E =      [32,  1,  2,  3,  4,  5,
               4,  5,  6,  7,  8,  9,
               8,  9, 10, 11, 12, 13,
              12, 13, 14, 15, 16, 17,
              16, 17, 18, 19, 20, 21,
              20, 21, 22, 23, 24, 25,
              24, 25, 26, 27, 28, 29,
              28, 29, 30, 31, 32,  1]

    # Permutation P within the f-function
    P = [16,  7, 20, 21, 29, 12, 28, 17,
          1, 15, 23, 26,  5, 18, 31, 10,
          2,  8, 24, 14, 32, 27,  3,  9,
         19, 13, 30,  6, 22, 11,  4, 25]


    # S-boxes for the data
    S = [
        [[14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
         [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
         [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
         [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]],

        [[15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
         [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
         [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
         [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]],

        [[10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
         [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
         [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
         [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]],

        [[ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
         [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
         [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
         [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]],

        [[ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
         [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
         [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
         [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]],

        [[12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
         [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
         [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
         [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]],

        [[ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
         [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
         [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
         [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]],

        [[13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
         [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
         [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
         [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]]
    ]

    # Initial key permutation PC-1 (permuted choice one)
    PC1 = [57, 49, 41, 33, 25, 17,  9,  1,
           58, 50, 42, 34, 26, 18, 10,  2,
           59, 51, 43, 35, 27, 19, 11,  3,
           60, 52, 44, 36, 63, 55, 47, 39,
           31, 23, 15,  7, 62, 54, 46, 38,
           30, 22, 14,  6, 61, 53, 45, 37,
           29, 21, 13,  5, 28, 20, 12,  4]

    # Round key permutation PC-2 (permuted choice two)
    PC2 = [14, 17, 11, 24,  1,  5,  3, 28,
           15,  6, 21, 10, 23, 19, 12,  4,
           26,  8, 16,  7, 27, 20, 13,  2,
           41, 52, 31, 37, 47, 55, 30, 40,
           51, 45, 33, 48, 44, 49, 39, 56,
           34, 53, 46, 42, 50, 36, 29, 32]

    # Key schedule round shifts
    K_SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def bitarray2str(bit_array): #Recreate the string from the bit array
    bits = [int(i) for i in bit_array.tolist()]
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b * 8 : (b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

# bitarray to int
bitarray2int = lambda bit_array: struct.unpack(">Q", bit_array)[0]

def int2bitarray(x):
    bit_array = bitarray(endian="big")
    bit_array.frombytes(struct.pack(">Q", x))
    return bit_array

def perm_unbalanced(x, p, m):
    B = bitarray(endian="big")
    bits_short = list(bin(x)[2:])
    nbits = m - len(bits_short)
    bits = (['0'] * nbits) + bits_short
    for i in p:
        B.append(int(bits[i]))
    return int.from_bytes(B.tobytes(), byteorder="big")

class DES(object):
    _string = None
    _key = None
    _words_L = {DES_nums.L: 0}
    _words_R = {DES_nums.R: 0}
    _key_halves_C = {DES_nums.C: 0}
    _key_halves_D = {DES_nums.D: 0}
    _sub_keys = {}

    @classmethod
    def encrypt(cls, string, key, padding=True):
        mode = "encrypt"
        if len(key) < 8:
            raise "Key should be at least 8 bytes long."
        elif len(key) > 8:
            key = key[:8] # For keys longer than 8 bytes, use the first 8 bytes
        cls._string = string
        cls._key = key
        if padding:
            cls._add_padding() # Add padding
        padded_bit_array = cls._string2bits()
        cls._key_schedule(key) # Store scheduled keys
        N = len(padded_bit_array) // 64
        cipher = bitarray(endian="big")
        for chunk_index in range(N):
            start = chunk_index * 64
            chunked_bit_array = padded_bit_array[start:start+64]
            X = bitarray2int(chunked_bit_array) # Convert 'bitarray' objects to integers.
            Y = cls._init_perm(X) # Apply initial permutation
            cls._rounds(Y, mode) # Fiestel network for 16 rounds
            Z = bin(cls._final_perm())[2:] # Final permutation
            nZ = len(Z)
            Z = ('0' * (64 - nZ)) + Z
            for c in Z:
                cipher.append(int(c))
        return bitarray2str(cipher)

    @classmethod
    def decrypt(cls, string, key, padding=True):
        mode = "decrypt"
        if len(key) < 8:
            raise "Key should be at least 8 bytes long."
        elif len(key) > 8:
            key = key[:8] # For keys longer than 8 bytes, use the first 8 bytes
        cls._string = string
        cls._key = key
        unpadded_bit_array = cls._string2bits()
        cls._key_schedule(key) # Store scheduled keys
        N = len(unpadded_bit_array) // 64
        plain_text = bitarray(endian="big")
        for chunk_index in range(N):
            start = chunk_index * 64
            chunked_bit_array = unpadded_bit_array[start:start+64]
            X = bitarray2int(chunked_bit_array) # Convert 'bitarray' objects to integers.
            Y = cls._init_perm(X) # Apply initial permutation
            cls._rounds(Y, mode) # Fiestel network for 16 rounds
            Z = bin(cls._final_perm())[2:] # Final permutation
            nZ = len(Z)
            Z = ('0' * (64 - nZ)) + Z
            for c in Z:
                plain_text.append(int(c))
        if padding:
            res = cls._remove_padding(bitarray2str(plain_text))
        else:
            res = bitarray2str(plain_text)
        return res

    # Add PKCS5 padding
    @classmethod
    def _add_padding(cls):
        len_pad = 8 - (len(cls._string) % 8)
        cls._string = cls._string + chr(len_pad) * len_pad
        return None

    # Remove PKCS5 padding
    @classmethod
    def _remove_padding(cls, string):
        len_pad = ord(string[-1])
        return string[:-len_pad]

    @classmethod
    def _string2bits(cls):
        lst = []
        for c in cls._string:
            bits = bin(ord(c))[2:]
            bits = '00000000'[len(bits):] + bits
            lst.extend([int(b) for b in bits])
        return bitarray(lst)

    # Define subkey function for 16 rounds
    @classmethod
    def _key_schedule(cls, key):
        # Key string to bits
        def string2bits(string):
            lst = []
            for c in string:
                bits = bin(ord(c))[2:]
                bits = '00000000'[len(bits):] + bits
                lst.extend([int(b) for b in bits])
            return bitarray(lst)
        # Define 28-bit splitting function
        def key_split(Y):
            R = Y & 0xfffffff
            L = (Y >> 28) & 0xfffffff
            return [L, R]
        # Rotate cyclically left by 1 or 2 bits
        def rot(x, b):
            r = (x << b) & 0xfffffff
            r = r ^ (x >> (28 - b))
            return r
        k_mux = lambda C, D: (C << 28) ^ D # Multiplex eight 28-bit blocks into a 56-bit block
        key_bits = string2bits(key) # Convert key string to integer
        K = struct.unpack(">Q", key_bits)[0]
        PC1 = DES_tables.PC1.value # PC-1
        p = [i - 1 for i in PC1]
        K_pc1 = perm_unbalanced(K, p, 64)
        [C0, D0] = key_split(K_pc1) # Split key
        cls._key_halves_C[DES_nums.C] = C0
        cls._key_halves_D[DES_nums.D] = D0
        shift = DES_tables.K_SHIFT.value
        for i in range(1, 17): # For rounds 1-16
            cls._key_halves_C[DES_nums.C] = rot(cls._key_halves_C[DES_nums.C], shift[i-1])
            cls._key_halves_D[DES_nums.D] = rot(cls._key_halves_D[DES_nums.D], shift[i-1])
            k_rot = k_mux(cls._key_halves_C[DES_nums.C],
                       cls._key_halves_D[DES_nums.D])
            p = [j - 1 for j in DES_tables.PC2.value]
            cls._sub_keys[i] = perm_unbalanced(k_rot, p, 56)
        return None

    # Initial permutation for the data
    @classmethod
    def _init_perm(cls, x):
        IP = DES_tables.IP.value
        p = [i - 1 for i in IP]
        return perm_unbalanced(x, p, 64)

    # DES rounds
    @classmethod
    def _rounds(cls, Y, mode):
        # Define 32-bit splitting function
        def word_split(Y):
            bit_array = bitarray(endian="big")
            bit_array.frombytes(struct.pack(">Q", Y))
            L = struct.unpack(">I", bit_array[:32])[0]
            R = struct.unpack(">I", bit_array[-32:])[0]
            return [L, R]
        # Demultiplex 48 bytes into eight 6-bit blocks
        def demux(x):
            y = []
            for i in range(8):
                y.append((x >> (7 - i) * 6) & 0x3f)
            return y
        # Multiplex eight 4-bit blocks into a 32-bit block
        def mux(x):
            y = 0
            for i, u in enumerate(x):
                y = y ^ (u << ((7 - i) * 4))
            return y
        # Substitution boxes function
        def sbox(box_num, x):
            S = DES_tables.S.value
            r, c = 0, 0
            r = r ^ (x & 1)
            r = r ^ ((x >> 4) & 2)
            c = c ^ ((x >> 1) & 15)
            return S[box_num][r][c]
        # Define f-function
        def F(R, k):
            p = [i - 1 for i in DES_tables.E.value] # Expansion block
            R_exp = perm_unbalanced(R, p, 32)
            Q = R_exp ^ k # XOR with the subkey
            U = demux(Q) # Demultiplex into eight 6-bit blocks
            W = []
            for i, u in enumerate(U): # Pass through substitution boxes S1-S8
                W.append(sbox(i, u))
            Z = mux(W) # Join the eight 4-bit boxes
            P = DES_tables.P.value # F-function permutation
            p = [i - 1 for i in P]
            fval = perm_unbalanced(Z, p, 32)
            return fval

        [L0, R0] = word_split(Y) # Split the input into 2 halves
        cls._words_L[DES_nums.L] = L0
        cls._words_R[DES_nums.R] = R0
        for rnd in range(1, 17): # 16 DES rounds
            if mode == "encrypt":
                subkey = cls._sub_keys[rnd]
            elif mode == "decrypt":
                subkey = cls._sub_keys[17 - rnd]
            tmp = cls._words_R[DES_nums.R]
            cls._words_R[DES_nums.R] = cls._words_L[DES_nums.L] ^ F(tmp, subkey)
            cls._words_L[DES_nums.L] = tmp
        return None

    @classmethod
    def _final_perm(cls):
        R = cls._words_L[DES_nums.L]
        L = cls._words_R[DES_nums.R]
        w = (L << 32) ^ R
        p = [i - 1 for i in DES_tables.IP_inv.value]
        return perm_unbalanced(w, p, 64)
