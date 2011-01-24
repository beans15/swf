# -*- coding: utf-8 -*-

import re

from contextlib import closing
from urllib import urlencode
from urllib2 import urlopen

from base import BaseBrowser
from swf.parser import Parser
from swf.tags import TAG_DEFINE_EDIT_TEXT


class UtamapBrowser(BaseBrowser):
    def get_music_id(self, url):
        regex = re.compile(r'^.+\?surl=(?P<music_id>.+)$')
        match = regex.match(url)
        if not match:
            raise ValueError('Invalid url was specified.')
        return match.group('music_id')

    def get_lyric(self, music_id):
        url = self.get_download_url(music_id)
        with closing(urlopen(url)) as response:
            # Replacing new-line to null character for regex matching.
            text = response.read().replace("\n", "\0")
            regex = re.compile(r'test1=(?P<id>.+?)&test2=(?P<lyric>.+)')
            match = regex.match(text)
            if match:
                lyric = match.group('lyric').replace("\0", "\n")
                encodings = ('utf-8', 'shift-jis', 'iso-2022-jp', 'euc-jp')
                for encoding in encodings:
                    try:
                        return lyric.decode(encoding)
                    except UnicodeDecodeError:
                        pass
            return None

    def get_download_url(self, music_id):
        return 'http://www.utamap.com/phpflash/flashfalsephp.php?unum=%s' \
            % music_id
