# -*- coding: utf-8 -*-

import re

from contextlib import closing
from urllib import urlencode
from urllib2 import urlopen, Request

from base import BaseBrowser
from parser import Parser
from tags import TAG_DEFINE_EDIT_TEXT


class UtaNetBrowser(BaseBrowser):
    def get_lyric(self, music_id):
        swf = self.get_swf(music_id)
        parser = Parser(swf)
        for tag in parser.tags:
            if tag.tag_type == TAG_DEFINE_EDIT_TEXT:
                return tag.content.initial_text

    def get_music_id(self, lyric_url):
        regex = re.compile(r'^.+\?ID=(?P<music_id>\d+)$')
        match = regex.match(lyric_url)
        if not match:
            raise ValueError('Invalid url was specified.')
        return int(match.group('music_id'))

    def get_swf(self, music_id):
        url = self.get_download_url(music_id)
        referer = self.get_lyric_url(music_id)

        request = Request(url)
        request.add_header('Referer', referer)

        with closing(urlopen(request)) as response:
            return response.read()

    def get_lyric_url(self, music_id):
        """Get url of the page where the lyric is shown."""
        return 'http://www.uta-net.com/user/phplib/view_0.php?ID=%d' \
            % music_id

    def get_download_url(self, music_id):
        """Get url to download lyric swf."""
        return ('http://www.uta-net.com/user/phplib/swf/showkasi.php'
            '?ID=%d&WIDTH=530&HEIGHT=770&FONTSIZE=14&t=1295422444') % music_id
