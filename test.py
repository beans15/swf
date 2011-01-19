#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from browser import UtaNetBrowser


def get_lyric(url):
    browser = UtaNetBrowser()
    music_id = browser.get_music_id(url)
    return browser.get_lyric(music_id)

if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) >= 1:
        url = argv[0]
    else:
        url = raw_input('Please input the url: ')

    print get_lyric(url)

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
