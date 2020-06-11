from bitarray import bitarray
import sys

sys.path.insert(1, '/home/chholak/Git/Cryptography/Chapter4')
from des import DES, bitarray2int, bitarray2str

def string2bits(string):
    lst = []
    for c in string:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        lst.extend([int(b) for b in bits])
    return bitarray(lst)

class lmdes:
    """
    Microsoft LAN Manager password hashing using DES.
    """
    def __init__(self, word):
        self.text = "KGS!@#$%"
        self.pwd = word
        self.key1 = ''
        self.key2 = ''
        self.deskey = ''

    def _pad_key(self):
        pwd = self.pwd.upper() # Convert to uppercase
        bit_array = string2bits(pwd)
        bits = [int(x) for x in bit_array.tolist()]
        bits_exp = list("".join(str(b) + '0' * (n % 7 == 6)
                                 for n, b in enumerate(bits)))
        bits_exp = [int(x) for x in bits_exp]
        self.deskey = bitarray2str(bitarray(bits_exp))

    def _get_keys(self):
        # Convert to uppercase
        pwd = self.pwd.upper()
        # Add null padding to fill 14 bytes and then after every 7 bits
        null_bytes = 14 - len(pwd)
        bit_array = string2bits(pwd)
        for i in range(null_bytes * 8):
            bit_array.append(0)
        bits = [int(x) for x in bit_array.tolist()]
        bits_exp = list("".join(str(b) + '0' * (n % 7 == 6)
                                 for n, b in enumerate(bits)))
        bits_exp = [int(x) for x in bits_exp]
        key = bitarray2str(bitarray(bits_exp))
        self.key1, self.key2 = key[:8], key[8:]

    def hexdigest(self):
        self._pad_key()
        c = DES.encrypt(self.text, self.deskey, padding=False)
        zeros = '0' * 16
        h = hex(bitarray2int(string2bits(c)))[2:]
        return zeros[len(h):] + h

    def generate_hash(self):
        self._get_keys()
        c1 = DES.encrypt(self.text, self.key1, padding=False)
        c2 = DES.encrypt(self.text, self.key2, padding=False)
        zeros = '0' * 16
        h1 = hex(bitarray2int(string2bits(c1)))[2:]
        h1 = zeros[len(h1):] + h1
        h2 = hex(bitarray2int(string2bits(c2)))[2:]
        h2 = zeros[len(h2):] + h2
        return h1 + h2
