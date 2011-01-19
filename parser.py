# -*- coding: utf-8 -*-

import math

from datatypes import Rect
from itertools import islice
from struct import unpack
from tags import TAG_END, TAGS


class Parser(object):
    def __init__(self, data):
        self.data = data
        self.header = Header(data)

        tags = []
        end = self.header.tell()
        sliced_data = islice(data, end, None)
        while True:
            tag = Tag(sliced_data)
            tags.append(tag)

            end += tag.tell()
            if tag.tag_type == TAG_END:
                break

        self.tags = tags


class Header(object):
    def __init__(self, data):
        self.data = data

        self.is_compressed = data[0] == 'C'
        self.version = ord(data[3])
        self.file_size = unpack('<L', data[4:8])[0]

        self.frame_size = Rect(islice(data, 8, None))
        index = 8 + self.frame_size.tell()

        self.frame_rate = unpack('<H', data[index:index + 2])[0] / 256.0
        self.frame_count = unpack('<H', data[index + 2:index + 4])[0]

        self.end = index + 4

    def tell(self):
        """ヘッダが占めるバイト数を返す"""
        return self.end


class Tag(object):
    def __init__(self, data):
        data = iter(data)
        tag_code_and_length = unpack('<H', ''.join(islice(data, 2)))[0]
        tag_type = tag_code_and_length >> 6
        tag_length = tag_code_and_length & (2 ** 6 - 1)
        end = 1

        if tag_length == 0x3f:
            # long style
            tag_length = unpack('<l', ''.join(islice(data, 4)))[0]
            end += 1

        self.tag_type = tag_type
        self.tag_length = tag_length

        self.content_value = ''.join(islice(data, tag_length))
        klass = dict(TAGS)[self.tag_type]
        try:
            self.content = klass(self.content_value)
        except NotImplementedError:
            self.content = None

        self.end = end + tag_length

    def tell(self):
        """このタグが占めるバイト数を返す"""
        return self.end
