# Part 1 goes here!
class ChunkError(Exception):
    pass
class DecodeError(Exception):
    pass
class BitList:
    def __init__(self, s):
        if not isinstance(s, str):
            raise ValueError('s not string')
        for c in s:
            if c != '0' and c != '1':
                raise ValueError('Format is invalid; does not consist of only 0 and 1')
        self.s = s
    def __eq__(self, o):
        if not isinstance(o, BitList):
            return False
        return self.s == o.s
    @staticmethod
    def from_ints(*args):
        s = ""
        for n in args:
            if not isinstance(n, int):
                raise ValueError('n not int')
            if n != 0 and n != 1:
                raise ValueError('Format is invalid; does not consist of only 0 and 1')
            s += str(n)
        return BitList(s)
    def __str__(self):
        return self.s
    def arithmetic_shift_left(self):
        self.s = self.s[1:] + "0"
    def arithmetic_shift_right(self):
        self.s = self.s[0] + self.s[:-1]
    def bitwise_and(self, o):
        if not isinstance(o, BitList):
            raise ValueError('o not BitList')
        if len(o.s) != len(self.s):
            raise ValueError('must equal length')
        k = ''
        for i in range(len(self.s)):
            if self.s[i] == '1' and o.s[i] == '1':
                k += '1'
            else:
                k += '0'
        return BitList(k)
    def chunk(self, l):
        if len(self.s) % l != 0:
            raise ChunkError()
        ans = []
        for i in range(0, len(self.s), l):
            t = []
            for c in range(i, i + l):
                t.append(int(self.s[c]))
            ans.append(t)
        return ans
    def decode(self, encoding='utf-8'):
        if encoding != 'utf-8' and encoding != 'us-ascii':
            raise ValueError(' encoding is not supported')
        if encoding == 'utf-8':
            if len(self.s) % 8 != 0:
                raise DecodeError()
            l = self.chunk(8)
            i = 0
            ans = ""
            while i < len(l):
                stri = "".join([str(x) for x in l[i]])
                if stri[0] == '0':
                    ans += chr(int(stri, 2))
                    i += 1
                elif stri.startswith("110"):
                    strj = "".join([str(x) for x in l[i+1]])
                    if not strj.startswith("10"):
                        raise DecodeError()
                    ans += chr(int(stri[3:] + strj[2:], 2))
                    i += 2
                elif stri.startswith("1110"):
                    strj = "".join([str(x) for x in l[i+1]])
                    strk = "".join([str(x) for x in l[i+2]])
                    if not strj.startswith("10") or not strk.startswith("10"):
                        raise DecodeError()
                    ans += chr(int(stri[4:] + strj[2:] + strk[2:], 2))
                    i += 3
                elif stri.startswith("11110"):
                    strj = "".join([str(x) for x in l[i+1]])
                    strk = "".join([str(x) for x in l[i+2]])
                    strm = "".join([str(x) for x in l[i+3]])
                    if not strj.startswith("10") or not strk.startswith("10") or not strm.startswith("10"):
                        raise DecodeError()
                    #print(stri[3:] + strj[2:] + strk[2:] + strm[2:], 2)
                    ans += chr(int(stri[5:] + strj[2:] + strk[2:] + strm[2:], 2))
                    i += 4
                else:
                    raise DecodeError()
            return ans
                        
        else:
            if len(self.s) % 7 != 0:
                raise DecodeError()
            ans = ""
            for l in self.chunk(7):
                ans += chr(int("".join([str(x) for x in l]), 2))
            return ans
                
            
    
        

