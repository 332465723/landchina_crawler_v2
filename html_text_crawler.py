# -*- coding: utf-8 -*-

import re
import urllib2
import os

from fonts_decoder.fonts_decoder import FontDecoder
from drivers.crawler_driver import CD
from setting import base_dir

def get_web_html(target_url):
    html_text = CD.get_html(target_url)
    html_text = html_text.decode('gbk')

    match = re.search(ur'styles\/fonts\/(.*.woff)\?', html_text)
    if match:
        try:
            font_url = 'http://landchina.com/styles/fonts/' + match.group(1)
            # TODO download fontfile
            r = urllib2.Request(font_url, headers=crawler_headers.common_headers)
            response = urllib2.urlopen(r)
            font_content = response.read()
            font_file_path = os.path.join(base_dir, 'download_fonts/%s' % match.group(1))
            with open(font_file_path, 'wb') as fp:
                fp.write(font_content)
            fd = FontDecoder(obj_font_file_path=font_file_path)

            word_map = fd.generate_word_map()
            for code in word_map:
                html_text = html_text.replace(code, word_map[code])
        except Exception as e:
            print('WOFF of target_url[%s] is bad bad!' % target_url)
            print(font_url)
            pass

    return html_text
