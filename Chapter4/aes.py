from enum import Enum

class AES_tables(Enum):
    SBOX = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
            0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
            0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
            0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
            0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
            0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
            0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
            0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
            0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
            0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
            0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
            0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
            0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
            0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
            0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
            0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,]

    SBOX_INV = [0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
                0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
                0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
                0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
                0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
                0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
                0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
                0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
                0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
                0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
                0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
                0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
                0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
                0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
                0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
                0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,]

    RCON = [
        0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
        0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
        0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
        0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
    ]

#########################################################
# Hex to state matrix conversion and vice versa
#########################################################
def hex2state(text):
    '''
    This function takes a 128-bit block and translates it into
    a state matrix where each column is a 4-byte word
    The inputs should be hex presented as strings
    '''
    state = []
    for i in range(16):
        byte = int(text[i * 2 : (i * 2) + 2], 16) #Operates on two hex chars at a time
        if i % 4 == 0:
            state.append([byte])
        else:
            state[i // 4].append(byte)
    return state

def state2hex(state):
    '''
    Reverses text2state to output either ciphertext or plaintext as a
    HEX string (ex: '5233ffaa')
    '''
    text = ''
    for column in state:
        for byte in column:
            val1 = "%x" % (byte >> 4)
            val2 = "%x" % (byte & 0xF)
            text = text + val1 + val2
    return text

#########################################################
# String to hex conversion and vice versa
#########################################################
string2hex = lambda x: "".join((hex(ord(c))[2:].zfill(2) for c in x))

def hex2string(x):
    chars = []
    for b in range(len(x) // 2):
        byte = x[b * 2 : (b + 1) * 2]
        chars.append(chr(int(byte, 16)))
    return "".join(chars)

#########################################################
# Helper function for mix columns and its inverse
#########################################################
def xtime(a, n=1):
    for i in range(n):
        if a & 0x80:
            a = a << 1
            a ^= 0x1B
        else:
            a = a << 1
    return a & 0xFF

class AES(object):
    _text = None
    _key = None
    _state = [[]]
    _sub_keys = [[]]

    #########################################################
    # Add/Remove PKCS5 padding
    #########################################################
    @classmethod
    def _pad(cls):
        s = cls._text
        return s + chr(16 - len(s) % 16) * (16 - len(s) % 16)

    @classmethod
    def _unpad(cls, string):
        return string[:-ord(string[-1])]

    #########################################################
    # Key expansion
    #########################################################
    @classmethod
    def _key_expansion(cls):
        def rot_words(w):
            w[0], w[1], w[2], w[3] = w[1], w[2], w[3], w[0]
            return w
        def sub_words(w):
            sbox = AES_tables.SBOX.value
            for i in range(4):
                w[i] = sbox[w[i]]
            return w
        Nb, Nr, Nk = 4, 10, 4
        w = hex2state(string2hex(cls._key))
        i = Nk
        while len(w) < Nb * (Nr + 1):
            w.append([0, 0, 0, 0])
        rcon = AES_tables.RCON.value
        while i < Nb * (Nr + 1):
            temp = w[i - 1][:]
            if i % Nk == 0:
                temp = sub_words(rot_words(temp))
                temp[0] = temp[0] ^ rcon[i // Nk]
            for x in range(4):
                w[i][x] = w[i - Nk][x] ^ temp[x]
            i += 1
        cls._sub_keys = w
        return None

    #########################################################
    # Block encryption round functions
    #########################################################
    @classmethod
    def _add_round_key(cls, r):
        k = cls._sub_keys[r * 4 : (r + 1) * 4]
        for i in range(4):
            for j in range(4):
                cls._state[i][j] ^= k[i][j]
        return None

    @classmethod
    def _sub_bytes(cls):
        sbox = AES_tables.SBOX.value
        for i in range(4):
            for j in range(4):
                cls._state[i][j] = sbox[cls._state[i][j]]
        return None

    @classmethod
    def _inv_sub_bytes(cls):
        sbox = AES_tables.SBOX_INV.value
        for i in range(4):
            for j in range(4):
                cls._state[i][j] = sbox[cls._state[i][j]]
        return None

    @classmethod
    def _shift_rows(cls):
        s = cls._state
        s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
        s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
        s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]
        cls._state = s
        return None

    @classmethod
    def _inv_shift_rows(cls):
        s = cls._state
        s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
        s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
        s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]
        cls._state
        return None

    @classmethod
    def _mix_columns(cls):
        def mix_a_column(s):
            u = s[0] ^ s[1] ^ s[2] ^ s[3]
            v = s[0]
            # XORing s[i] to itself cancels out the extra term in 'u'
            s[0] ^= xtime(s[0] ^ s[1]) ^ u
            s[1] ^= xtime(s[1] ^ s[2]) ^ u
            s[2] ^= xtime(s[2] ^ s[3]) ^ u
            s[3] ^= xtime(s[3] ^ v) ^ u
            return s
        for i in range(4):
            cls._state[i] = mix_a_column(cls._state[i])
        return None

    @classmethod
    def _inv_mix_columns(cls):
        def inv_mix_a_column(s):
            x = list(s)
            u = xtime(s[0], 3) ^ xtime(s[1], 3) ^ xtime(s[2], 3) ^ xtime(s[3], 3)
            x[0] = s[3] ^ xtime(s[0], 2) ^ xtime(s[0]) ^ xtime(s[1]) ^ s[1] ^ xtime(s[2], 2) ^ s[2] ^ u
            x[1] = s[0] ^ xtime(s[1], 2) ^ xtime(s[1]) ^ xtime(s[2]) ^ s[2] ^ xtime(s[3], 2) ^ s[3] ^ u
            x[2] = s[1] ^ xtime(s[2], 2) ^ xtime(s[2]) ^ xtime(s[3]) ^ s[3] ^ xtime(s[0], 2) ^ s[0] ^ u
            x[3] = s[2] ^ xtime(s[3], 2) ^ xtime(s[3]) ^ xtime(s[0]) ^ s[0] ^ xtime(s[1], 2) ^ s[1] ^ u
            return x
        for i in range(4):
            cls._state[i] = inv_mix_a_column(cls._state[i])
        return None

    #########################################################
    # Encryption in 128-bit blocks after PKCS5 padding
    #########################################################
    @classmethod
    def encrypt(cls, text, key):
        if len(key) < 16:
                raise "Key should be at least 16 bytes long."
        elif len(key) > 16:
            key = key[:16] # For keys longer than 16 bytes, use the first 16 bytes
        cls._text = text
        cls._key = key
        cls._key_expansion()
        padded_text = cls._pad()

        cipher = []
        N = len(padded_text) // 16
        for block_index in range(N):
            start = block_index * 16
            block = padded_text[start:start+16]
            for c in cls._encrypt_block(block):
                cipher.append(c)
        return "".join(cipher)

    @classmethod
    def decrypt(cls, text, key):
        if len(key) < 16:
                raise "Key should be at least 16 bytes long."
        elif len(key) > 16:
            key = key[:16] # For keys longer than 16 bytes, use the first 16 bytes
        cls._text = text
        cls._key = key
        cls._key_expansion()
        plain = []
        N = len(cls._text) // 32
        for block_index in range(N):
            start = block_index * 32
            block = cls._text[start:start+32]
            for p in cls._decrypt_block(block):
                plain.append(p)

        plain = hex2string("".join(plain))
        return cls._unpad(plain)

    @classmethod
    def _encrypt_block(cls, blk):
        cls._state = hex2state(string2hex(blk))
        cls._add_round_key(0)

        for r in range(1, 10):
            cls._sub_bytes()
            cls._shift_rows()
            cls._mix_columns()
            cls._add_round_key(r)

        cls._sub_bytes()
        cls._shift_rows()
        cls._add_round_key(10)

        return state2hex(cls._state)

    @classmethod
    def _decrypt_block(cls, blk):
        cls._state = hex2state(blk)
        cls._add_round_key(10)

        for r in range(9, 0, -1):
            cls._inv_shift_rows()
            cls._inv_sub_bytes()
            cls._add_round_key(r)
            cls._inv_mix_columns()

        cls._inv_shift_rows()
        cls._inv_sub_bytes()
        cls._add_round_key(0)

        return state2hex(cls._state)
