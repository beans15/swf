#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
# パスを通す
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '../')))

from browsers import UtaNetBrowser, UtamapBrowser
from parser import Parser
from tags import TAG_DEFINE_EDIT_TEXT


def get_lyric(url):
    browser = UtamapBrowser()
    music_id = browser.get_music_id(url)
    return browser.get_lyric(music_id)


if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) >= 1:
        url = argv[0]
    else:
        print >>sys.stderr, 'Please input the url: ',
        url = raw_input()

    print get_lyric(url).encode('utf-8')

    #with open('target.swf') as f:
    #    data = f.read()
    #parser = Parser(data)
    #header = parser.header
    ##print 'Compressed: %s' % header.is_compressed
    ##print 'Version: %d' % header.version
    ##print 'FileSize: %d bytes' % header.file_size
    ##print 'FrameSize: %d <= x <= %d, %d <= y <= %d' \
    ##    % (header.frame_size.x_min, header.frame_size.x_max,
    ##       header.frame_size.y_min, header.frame_size.y_max)
    ##print 'FrameRate: %.2f' % header.frame_rate
    ##print 'FrameCount: %d' % header.frame_count

    #for tag in parser.tags:
    #    if tag.tag_type == TAG_DEFINE_EDIT_TEXT:
    #        print tag.content.initial_text
