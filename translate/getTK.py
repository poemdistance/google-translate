# -*- coding: utf-8 -*-
import ast
import os
import pickle
import math
import re
import time
import requests
from termcolor import cprint

def rshift(val, n):                                                       
    #python port for '>>>'(right shift with padding
    return (val % 0x100000000) >> n

class TokenAcquirer(object):

    RE_TKK = re.compile(r'tkk:\'(.+?)\'', re.DOTALL)
    RE_RAWTKK = re.compile(r'tkk:\'(.+?)\'', re.DOTALL)

    def __init__(self, tkk='0', session=None, host='translate.google.cn', proxy=None, timeout=None):
        self.session = session or requests.Session()
        self.tkk = tkk
        self.proxy = proxy
        self.timeout = timeout
        self.host = host if 'http' in host else 'https://' + host

    def _update(self):

        # we don't need to update the base TKK value when it is still valid
        now = math.floor(int(time.time()) / 3600)

        if self.tkk == '0' and os.path.exists('./.tkk'):
            with open('./.tkk', 'rb') as f:
                self.tkk = pickle.load(f)
                #cprint('Found .tkk file, load firstly...', 'yellow')

        if self.tkk and int(self.tkk.split('.')[0]) == now:
            #if os.path.exists('./.tkk'):
                #cprint('Tkk still useful, will not change...', 'yellow')
            return

        r = self.session.get(self.host, proxies=self.proxy, timeout=self.timeout)

        raw_tkk = self.RE_TKK.search(r.text)
        if raw_tkk:
            self.tkk = raw_tkk.group(1)
            with open('./.tkk', 'wb') as f:
                pickle.dump(self.tkk, f)
                #cprint('Wrote tkk to .tkk file', 'yellow')
            return

    def _lazy(self, value):
        return lambda: value

    def _xr(self, a, b):
        size_b = len(b)
        c = 0
        while c < size_b - 2:
            d = b[c + 2]
            d = ord(d[0]) - 87 if 'a' <= d else int(d)
            d = rshift(a, d) if '+' == b[c + 1] else a << d
            a = a + d & 4294967295 if '+' == b[c] else a ^ d

            c += 3
        return a

    def acquire(self, text):
        a = []
        # Convert text to ints
        for i in text:
            val = ord(i)
            if val < 0x10000:
                a += [val]
            else:
                # Python doesn't natively use Unicode surrogates,
                # so account for those
                a += [
                    math.floor((val - 0x10000)/0x400 + 0xD800),
                    math.floor((val - 0x10000)%0x400 + 0xDC00)
                    ]

        b = self.tkk if self.tkk != '0' else ''
        d = b.split('.')
        b = int(d[0]) if len(d) > 1 else 0

        # assume e means char code array
        e = []
        g = 0
        size = len(text)
        while g < size:
            l = a[g]
            # just append if l is less than 128(ascii: DEL)
            if l < 128:
                e.append(l)
            # append calculated value if l is less than 2048
            else:
                if l < 2048:
                    e.append(l >> 6 | 192)
                else:
                    # append calculated value if l matches special condition
                    if (l & 64512) == 55296 and g + 1 < size and \
                            a[g + 1] & 64512 == 56320:
                        g += 1
                        l = 65536 + ((l & 1023) << 10) + (a[g] & 1023) # This bracket is important
                        e.append(l >> 18 | 240)
                        e.append(l >> 12 & 63 | 128)
                    else:
                        e.append(l >> 12 | 224)
                    e.append(l >> 6 & 63 | 128)
                e.append(l & 63 | 128)   
            g += 1
        a = b
        for i, value in enumerate(e):
            a += value
            a = self._xr(a, '+-a^+6')
        a = self._xr(a, '+-3^+b+-f')
        a ^= int(d[1]) if len(d) > 1 else 0
        if a < 0:  # pragma: nocover
            a = (a & 2147483647) + 2147483648
        a %= 1000000  # int(1E6)

        return '{}.{}'.format(a, a ^ b)

    def do(self, text):
        self._update()
        tk = self.acquire(text)
        return tk
