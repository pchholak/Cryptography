class DES(object):
    _string = None
    _words = {
        DES_nums.L: 0,
        DES_nums.R: 0,
    }
    _key_halves = {
        DES_nums.C: 0,
        DES_nums.D: 0,
    }
    _sub_keys = {}
    
    @classmethod
    def encrypt(cls, string, K):
        cls._string = string
        padded_bit_array = cls._padding(cls._string2bits())
        print("Padded bit array" ,padded_bit_array)
        
        # Store scheduled keys
        cls._key_schedule(K)
        print("Scheduled keys")
        print(cls._sub_keys)
        
        N = len(padded_bit_array) // 64
        cipher = bitarray(endian="little")
        for chunk_index in range(N):
            start = chunk_index * 64
            chunked_bit_array = padded_bit_array[start:start+64]
            print("Chunked bit array:", chunked_bit_array)
            
            # Convert 'bitarray' objects to integers.
            X = struct.unpack("<Q", chunked_bit_array)[0]
            print("Integer input", X)
            
            # Apply initial permutation
            Y = cls._init_perm(X)
            print("After initial permutation:", Y)
            
            # Fiestel network for 16 rounds
            cls._rounds(Y)
            print("L_16 = {}, R_16 = {}".format(
                cls._words[DES_nums.L], cls._words[DES_nums.R]))
            
            # Final permutation
            for c in bin(cls._final_perm())[2:]:
                cipher.append(int(c))
        return cipher
    
    @classmethod
    def _string2bits(cls):
        # Convert string to a bit array.
        bit_array = bitarray(endian="little")
        bit_array.frombytes(cls._string.encode("utf-8"))
        return bit_array
    
    # "OneAndZeroes" padding
    @classmethod
    def _padding(cls, bit_array):
        bit_array.append(1)
        while bit_array.length() % 64 != 0:
            bit_array.append(0)
        return bit_array
    
    # Initial permutation for the data
    @classmethod
    def _init_perm(cls, x):
        IP = DES_tables.IP.value
        p = [i - 1 for i in IP]
        return perm(x, p)
    
    # DES rounds
    @classmethod
    def _rounds(cls, Y):
        # Define 32-bit splitting function
        def word_split(Y):
            bit_array = bitarray(endian="little")
            bit_array.frombytes(struct.pack("<Q", Y))
            L = struct.unpack("<I", bit_array[:32])[0]
            R = struct.unpack("<I", bit_array[-32:])[0]
            print("Initial split! L0 = {}, R0 = {}".format(L, R))
            return [L, R]
        
        # Demultiplex 48 bytes into eight 6-bit blocks
        def demux(x):
            y = []
            for i in range(8):
                y.append((x >> i) & 0x3f)
            return y
        
        # Multiplex eight 4-bit blocks into a 32-bit block
        def mux(x):
            y = 0
            for i, u in enumerate(x):
                y = y ^ (u << (i * 4))
            return y
        
        def sbox(box_num, x):
            S = DES_tables.S.value
            # Row and column select
            r, c = 0, 0
            r = r ^ (x & 1)
            c = c ^ ((x >> 1) & 15)
            r = r ^ ((x >> 4) & 2)
            return S[box_num][r][c]
        
        # Define f-function
        def F(R, k):
            # Expansion block
            p = [i - 1 for i in DES_tables.E.value]
            R_exp = perm_unbalanced(R, p, 32)
            
            # XOR with the subkey
            Q = R_exp ^ k
            
            # Demultiplex into eight 6-bit blocks
            U = demux(Q)
            
            # Pass through substitution boxes S1-S8
            # Note: MSB block goes in first
            W = []
            V = [t for t in reversed(U)]
            for i, v in enumerate(V):
                W.append(sbox(i, v))
                
            # Join the eight 4-bit boxes
            Z = mux(W)
            
            # F-function permutation
            P = DES_tables.P.value
            p = [i - 1 for i in P]
            fval = perm(Z, p)
            
            return fval
        
        # Split the input into 2 halves
        [L0, R0] = word_split(Y)
        cls._words[DES_nums.L.value] = L0
        cls._words[DES_nums.R.value] = R0
        print(cls._words)
        print("L_0 = {}, R_0 = {}".format(
            cls._words[DES_nums.L], cls._words[DES_nums.R]))
        
        # 16 DES rounds
        for rnd in range(1, 17):
            subkey = cls._sub_keys[rnd]
            print("subkey #{} = {}".format(rnd, subkey))
            tmp = cls._words[DES_nums.R]
            print("R_i-1 = {}".format(tmp))
            print("L_i-1 = {}".format(cls._words[DES_nums.L]))
            cls._words[DES_nums.R] = cls._words[DES_nums.L] ^ F(tmp, subkey)
            cls._words[DES_nums.L] = tmp
            print("L_{} = {}, R_{} = {}".format(
                rnd, cls._words[DES_nums.L], rnd, cls._words[DES_nums.R]))
    
    @classmethod
    def _final_perm(cls):
        R = cls._words[DES_nums.L]
        L = cls._words[DES_nums.R]
        w = (L << 32) ^ R
        p = [i - 1 for i in DES_tables.IP_inv.value]
        return perm(w, p)
    
    # Define subkey function for 16 rounds
    @classmethod
    def _key_schedule(cls, K):
        # Define 28-bit splitting function
        def key_split(Y):
            R = Y & 0xfffffff
            L = (Y >> 28) & 0xffffffff
            return [L, R]

        # Rotate cyclically left by 1 or 2 bits
        def rot(x, b):
            r = (x << b) & 0xfffffff
            r = r ^ (x >> (28 - b))
            return r

        # Multiplex eight 28-bit blocks into a 56-bit block
        k_mux = lambda C, D: (C << 28) ^ D

        # PC-1
        PC1 = DES_tables.PC1.value
        p = [i - 1 for i in PC1]
        K_pc1 = perm_unbalanced(K, p, 64)

        # Split key
        [C0, D0] = key_split(K_pc1)
        cls._key_halves[DES_nums.C] = C0
        cls._key_halves[DES_nums.D] = D0

        # For rounds 1-16
        for i in range(1, 17):
            if i in [1, 2, 9, 16]:
                cls._key_halves[DES_nums.C] = rot(cls._key_halves[DES_nums.C], 2)
                cls._key_halves[DES_nums.D] = rot(cls._key_halves[DES_nums.D], 2)
                k_rot = k_mux(cls._key_halves[DES_nums.C],
                           cls._key_halves[DES_nums.D])
                p = [i - 1 for i in DES_tables.PC2.value]
                cls._sub_keys[i] = perm_unbalanced(k_rot, p, 56)
            else:
                cls._key_halves[DES_nums.C] = rot(cls._key_halves[DES_nums.C], 1)
                cls._key_halves[DES_nums.D] = rot(cls._key_halves[DES_nums.D], 1)
                k_rot = k_mux(cls._key_halves[DES_nums.C],
                           cls._key_halves[DES_nums.D])
                p = [i - 1 for i in DES_tables.PC2.value]
                cls._sub_keys[i] = perm_unbalanced(k_rot, p, 64)
        return None

def perm(x, p):
    y = 0
    for q in range(len(p)):
        if (x & (1 << q)) != 0:
            y = y ^ (1 << p[q])
    return y

def perm_unbalanced(x, p, m):
    B = bitarray(endian="little")
    bits_short = list(bin(x)[2:])
    nbits = m - len(bits_short)
    bits = (['0'] * nbits) + bits_short
    bits.reverse()
    for i in p:
        B.append(int(bits[i]))
    return int.from_bytes(B.tobytes(), byteorder="little")
