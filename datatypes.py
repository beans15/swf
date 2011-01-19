# -*- coding: utf-8 -*-

import math

from itertools import islice
from notation import convert_byte_to_bin


class BaseDataType(object):
    end = 0

    def __init__(self, data):
        pass

    def tell(self):
        """渡されたデータのうち、このDataTypeが占めるバイト数を返す"""
        return self.end


class Rect(BaseDataType):
    """SWFのRECT構造をロードする"""
    def __init__(self, data):
        data = iter(data)
        first_byte = next(data)
        nbits = ord(first_byte) >> 3
        byte_length = int(math.ceil((5 + (nbits * 4)) / 8.0))
        rect_data = first_byte + ''.join(islice(data, byte_length - 1))

        rect_bytes = [ord(c) for c in rect_data]
        rect_bins = ''.join(convert_byte_to_bin(n) for n in rect_bytes)

        values = []
        bit_index = 5
        for i in xrange(0, 4):
            twips = int(rect_bins[bit_index:bit_index + nbits], 2)
            values.append(int(twips / 20.0))
            bit_index += nbits

        (self.x_min, self.x_max, self.y_min, self.y_max) = values
        self.end = byte_length


class RGB(BaseDataType):
    """SWFのRGB構造をロードする"""
    def __init__(self, data):
        data = iter(data)
        (self.red, self.green, self.blue) = \
            tuple(ord(c) for c in islice(data, 3))
        self.end = 3


class RGBA(BaseDataType):
    """SWFのRGBA構造をロードする"""
    def __init__(self, data):
        data = iter(data)
        (self.red, self.green, self.blue, self.alpha) = \
            tuple(ord(c) for c in islice(data, 4))
        self.end = 4


class ARGB(BaseDataType):
    """SWFのARGB構造をロードする"""
    def __init__(self, data):
        data = iter(data)
        (self.alpha, self.red, self.green, self.blue) = \
            tuple(ord(c) for c in islice(data, 4))
        self.end = 4


class String(BaseDataType):
    """SWFのSTRING構造をロードする"""
    def __init__(self, data):
        data = iter(data)

        def generate_chars():
            for c in data:
                if c == "\0":
                    break
                else:
                    yield c

        string = ''.join(generate_chars())

        # バージョンとか気にしない
        encodings = ('UTF-8', 'ASCII', 'SHIFT-JIS')
        for encoding in encodings:
            try:
                self.string = string.decode(encoding)
                break
            except UnicodeDecodeError:
                pass
        else:
            raise RuntimeError('Irregal encoding is used.')

        self.end = len(string) + 1

    def __unicode__(self):
        return self.string

    def __str__(self):
        return self.string.encode('UTF-8')
