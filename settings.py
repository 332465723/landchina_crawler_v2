# -*- coding: utf-8 -*-

import os


base_dir = os.path.dirname(os.path.abspath(__file__))
download_fonts_dir = os.path.join(base_dir, 'download_fonts')

if not os.path.exists(download_fonts_dir):
    os.mkdir(download_fonts_dir)
