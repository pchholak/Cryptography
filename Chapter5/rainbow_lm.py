# Adapted from: https://github.com/jfmengels/rainbowtable-python/

from lmdes import lmdes
from random import randrange

lettersUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = '0123456789'
allChars = lettersUpper + numbers

class RainbowTable:
    """
    Rainbow table: Structure to crack hashed passwords.
    """
    def __init__(self, columns=0, chars=allChars, pwdLength=7, rows=1000):
        """
        Initialises the rainbow table.
        columns:    Length of a chain, i.e. the number of times the password
                    at the start of the chain is hashed and reduced.
        chars:      List of characters covered.
        pwdLength:  Length of the passwords.
        rows:       Number of chains.
        """
        from RB import RBTree, rbnode
        self.table = RBTree()
        if columns > 0:
            self.columns = columns
            self.chars = chars
            self.pwdLength = pwdLength
            self.func = lmdes
            for i in range(rows):
                pwd = self.randomPassword()
                hashV = self.createChain(pwd)
                self.table.insert(hashV, pwd)

    def __repr__(self):
        """
        Prints the content of the table
        """
        return repr(self.table._root)

    def writeToFile(self, output):
        """
        Writes rainbow table into a file, so that it can be recovered at a
        different time later.
        output:  Name of the file to write to.
        """
        f = open(output, 'w')
        data = [self.columns, self.chars, self.pwdLength, self.func.__name__]
        data = [str(x) for x in data]
        f.write(" ".join(data))
        f.write("\n")
        f.write(repr(self))
        f.close()

    def readFromFile(self, inp):
        """
        Read a rainbow table from a file.
        input:  Name of the file to read from.
        """
        f = open(inp, "r")
        line = f.readline()
        line = line.strip().split(sep=" ", maxsplit=3)
        self.columns, self.chars, self.pwdLength, _ = line
        self.columns = int(self.columns)
        self.pwdLength = int(self.pwdLength)
        self.func = lmdes
        line = f.readline()
        while line != '':
            pwd, hashV = line.strip().split(sep=" ", maxsplit=1)
            self.table.insert(hashV, pwd)
            line = f.readline()
        f.close()

    def _find(self, hashV):
        """
        Find the passwords in the table corresponding to the given hash.
        hashV:  Hash to find.
        Returns a list of corresponding starting passwords.
        """
        return self.table.search(hashV)

    def hashWord(self, word):
        """
        Hash a 7 character word using LM hashing.
        word:  Word to hash.
        Returns the hash of the word.
        """
        return self.func(word).hexdigest()

    def reduce(self, hashV, column):
        """
        Reduce a hash.
        hashV:  Hash to reduce.
        column:  Column to hash at.
        Returns a valid password.
        """
        results = []
        # Cast hash from str to int then decompose into bytes
        byteArray = self.getBytes(hashV)
        for i in range(self.pwdLength):
            index = byteArray[(i + column) % len(byteArray)]
            newChar = self.chars[index % len(self.chars)]
            results.append(newChar)
        return "".join(results)

    def getBytes(self, hashV):
        """
        Transforms a hash into a list of bytes.
        hashV:  Hash to transform into bytes.
        Returns a list of bytes.
        """
        results = []
        remaining = int(hashV, 16)
        while remaining > 0:
            results.append(remaining & 0xff)
            remaining >>= 8
        return results

    def createChain(self, pwd):
        """
        Creates a chain.
        pwd:  Password to start the chain with.
        Returns the hash at the end of the chain.
        """
        for col in range(self.columns):
            hashV = self.hashWord(pwd)
            pwd = self.reduce(hashV, col)
        return hashV

    def randomPassword(self):
        """
        Generates a random password.
        Return the generated password.
        """
        pwd = ""
        charsLength = len(self.chars)
        for i in range(self.pwdLength):
            pwd += self.chars[randrange(charsLength)]
        return pwd

    def crackHash(self, startHash):
        """
        Tries to crack a hash.
        startHash:  Hash to crack.
        Returns the resulting password, if one is found, '' otherwise.
        """
        for col in range(self.columns, -1, -1):
            hashV = self._getFinalHash(startHash, col)
            pwdList = self._find(hashV)
            for pwd in pwdList:
                resPwd = self._findHashInChain(pwd, startHash)
                if resPwd != None:
                    return resPwd
        return ''

    def _getFinalHash(self, startHash, startCol):
        """
        Finds the hash at the end of a chain, starting from a hash
        and at a given column.
        startHash:  Hash to start with.
        startCol:  Column to start from.
        Returns the hash at the end of a chain.
        """
        hashV = startHash
        for col in range(startCol, self.columns-1):
            pwd = self.reduce(hashV, col)
            hashV = self.hashWord(pwd)
        return hashV

    def _findHashInChain(self, startPwd, startHash):
        """
        Tries to find a hash in a chain.
        startPwd:  Password at the beginning of a chain.
        startHash: Hash to find.
        Returns the corresponding password if one is found, None otherwise.
        """
        hashV = self.hashWord(startPwd)
        if hashV == startHash:
            return startPwd
        col = 0
        # Hash and reduce until the password has been found or the end of
        # the chain has been reached.
        while col < self.columns:
            pwd = self.reduce(hashV, col)
            hashV = self.hashWord(pwd)
            if hashV == startHash:
                # If the password has been found, return it
                return pwd
            col += 1
        # If the password hasn't been found, return None.
        return None

    def testWord(self, word):
        """
        Tries to find a password from its hash.
        word:  Word to find.
        Return the result of trying to crack the password of the hash.
        Note - Only for testing purposes.
        """
        return self.crackHash(self.hashWord(word))
