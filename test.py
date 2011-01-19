#!/usr/bin/env python
# -*- coding: utf-8 -*-

from swf import Parser
from tags import TAG_DEFINE_EDIT_TEXT


if __name__ == '__main__':
    from browser import utanet

    url = 'http://www.uta-net.com/user/phplib/view_0.php?ID=74849'
    browser = utanet.Browser()
    music_id = browser.get_music_id(url)
    swf = browser.get_swf(music_id)
    with open('testswf.swf', 'w') as f:
        f.write(swf)

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
