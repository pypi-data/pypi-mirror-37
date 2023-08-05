import collections
import itertools
import base64


class Bs:
    @classmethod
    def from_base64(cls, b64):
        return cls(base64.b64decode(b64))

    @classmethod
    def from_int(cls, n):
        assert n >= 0, 'required a positive value'
        data = []
        while n:
            data.append(n % 256)
            n >>= 8
        return cls(data)

    @classmethod
    def from_hex(cls, hs):
        if hs.startswith('0x'):
            return cls.from_int(int(hs, 16))
        else:
            n = len(hs) + -len(hs) % 2
            hs = hs.ljust(n, '0')
            return cls(int(hs[i:i+2], 16) for i in range(0, len(hs), 2))

    @classmethod
    def from_bin(cls, bs):
        if bs.startswith('0b'):
            return cls.from_int(int(bs, 2))
        else:
            nb = (len(bs) + 7) // 8
            return cls.from_int(int(bs[::-1], 2)).ljust(nb, 0)
    
    @classmethod
    def load(cls, path):
        with open(path, 'rb') as f:
            return cls(f.read())

    def __init__(self, *objs, p=None, r=True):
        self._p = p
        self._r = r
        self.data = []
        for obj in objs:
            if isinstance(obj, collections.Iterable):
                for item in obj:
                    self._add_item(item)
            else:
                self._add_item(obj)
        self._correct()
    
    def __iter__(self):
        yield from self.data
    
    def __getitem__(self, i):
        return self.data[i]
    
    def __setitem__(self, i, n):
        if isinstance(i, slice):
            r = range(*i.indices(len(self)))
            n = n if type(n) is type(self) else type(self)(n)
            if len(r) > len(n) and n._r:
                n = n.repeat((len(r) + len(n) - 1) // len(n))
            elif len(r) < len(n) and n._r:
                n = n[:len(r)]
            elif len(r) > len(n) and n._p is not None:
                n = n.ljust(len(r), n._p)
            else:
                assert len(r) == len(n), \
                        'cannot set values to {}: r={}, p={}, l={}'.format(
                            r, n._r, n._p, len(n))
            for j, v in zip(r, n):
                self[j] = v
        else:
            n = type(self)(n)
            assert len(n) == 1, 'expected only one value'
            self.data[i] = n[0]
    
    def __repr__(self):
        to_hex = lambda b: hex(b)[2:].rjust(2, '0')
        btext = ', '.join(map(to_hex, self[:128]))
        btext += ', ...' if len(self) > 128 else ''
        return '<{} {}: [{}]>'.format(type(self).__name__, len(self), btext)
    
    def __str__(self):
        return self.str()
    
    def __bytes__(self):
        return self.bytes()
    
    def __int__(self):
        return self.int()
    
    def __index__(self):
        return self.int()
    
    def __bool__(self):
        return bool(self.int())
    
    def __len__(self):
        return len(self.data)
    
    def __neg__(self):
        return type(self)(-i for i in self)
    
    def __add__(self, obj):
        return self._operate(obj, lambda x, y: x + y)
    
    def __sub__(self, obj):
        return self - obj
    
    def __mul__(self, obj):
        return self._operate(obj, lambda x, y: x * y)

    def __div__(self, obj):
        return self._operate(obj, lambda x, y: x // y)
    
    def __floordiv__(self, obj):
        return self._operate(obj, lambda x, y: x // y)
    
    def __and__(self, obj):
        return self._operate(obj, lambda x, y: x & y)
    
    def __or__(self, obj):
        return self._operate(obj, lambda x, y: x | y)
    
    def __xor__(self, obj):
        return self._operate(obj, lambda x, y: x ^ y)
    
    def __not__(self):
        return type(self)(~i for i in self)
    
    def __matmul__(self, obj):
        tmp = type(self)(self)
        tmp._add_item(obj)
        tmp._correct()
        return tmp
    
    def __eq__(self, obj):
        return self.data == type(self)(obj).data

    def ljust(self, width, fill=0):
        return type(self)(bytes(self.data).ljust(width, bytes([fill])))
    
    def rjust(self, width, fill=0):
        return type(self)(bytes(self.data).rjust(width, bytes([fill])))
    
    def repeat(self, n):
        return type(self)(self.data * n)
    
    def reverse(self):
        return type(self)(reversed(self))

    def np(self):
        return type(self)(self, p=False, r=self._r)

    def p(self, p):
        return type(self)(self, p=p, r=self._r)
    
    def nr(self):
        return type(self)(self, p=self._p, r=False)
    
    def r(self):
        return type(self)(self, p=self._p, r=True)

    def str(self):
        return bytes(self.data).decode()

    def bytes(self):
        return bytes(self.data)

    def int(self):
        p, value = 1, 0
        for n in self.data:
            value += n * p
            p <<= 8
        return value

    def bin(self):
        return ''.join(bin(n)[2:].rjust(8, '0')[::-1] for n in self)
    
    def hex(self):
        return ''.join(hex(n)[2:].rjust(2, '0') for n in self)
    
    def base64(self):
        return base64.b64encode(bytes(self)).decode()

    def bits(self, every=1, last='keep'):
        bs = self.bin()
        z = len(bs) - len(bs) % every
        bs, end = bs[:z], bs[z:]
        bs = [bs[i:i+every] for i in range(0, len(bs), every)]
        if end:
            if last == 'pad0':
                bs.append(end.ljust(every, '0'))
            elif last == 'pad1':
                bs.append(end.ljust(every, '1'))
            elif last == 'keep':
                bs.append(end)
            elif last == 'drop':
                pass
        return bs
    
    def every(self, n, f=lambda i: i):
        return [f(type(self)(self[i:i+n])) for i in range(0, len(self), n)]

    def dump(self, path):
        with open(path, 'wb') as f:
            f.write(self.bytes())

    def _correct(self):
        for i in range(len(self)):
            self.data[i] %= 256

    def _add_item(self, item):
        assert isinstance(item, (int, collections.Iterable)), \
                'unexpected type: {}'.format(type(item))
        if isinstance(item, int):
            self.data.append(item)
        elif isinstance(item, str):
            self.data += list(item.encode())
        else:
            for i in item:
                self._add_item(i)

    def _operate(self, obj, func):
        obj = obj if isinstance(obj, type(self)) else type(self)(obj)
        if len(self) == len(obj):
            x, y = self, obj
        elif len(self) > len(obj) and obj._p is not None:
            x, y = self, obj.ljust(len(self), obj._p % 256)
        elif len(self) > len(obj) and self._p is not None:
            x, y = self.ljust(len(obj), self._p % 256), obj
        elif len(self) > len(obj) and obj._r:
            x, y = self, obj.repeat(len(self) // len(obj) + 1)[:len(self)]
        elif len(self) < len(obj) and self._r:
            x, y = self.repeat(len(obj) // len(self) + 1)[:len(obj)], obj
        else:
            assert False, 'length not matched: {}'.format((len(self), len(obj)))
        return type(self)(func(i, j) for i, j in zip(x, y))
