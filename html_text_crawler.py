# -*- coding: utf-8 -*-

import re
import os

from fonts_decoder.fonts_decoder import FontDecoder
from drivers.crawler_driver import CD

def get_web_html(target_url):
    html_text = CD.get_html(target_url)
    html_text = html_text.decode('gbk')

    match = re.search(ur'styles\/fonts\/(.*.woff)\?', html_text)
    if match:
        try:
            font_url = 'http://landchina.com/styles/fonts/' + match.group(1)
            # TODO download fontfile
            font_file_path = CD.download(font_url)
            if not os.path.isfile(font_file_path):
                raise Exception('Font file download error!')

            fd = FontDecoder(obj_font_file_path=font_file_path)

            word_map = fd.generate_word_map()
            for code in word_map:
                html_text = html_text.replace(code, word_map[code])
        except Exception as e:
            print('WOFF of target_url[%s] is bad bad!' % target_url)
            print(font_url)
            pass

    return html_text
