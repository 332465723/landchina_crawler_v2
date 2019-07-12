# -*- coding: utf-8 -*-

import sys
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
try:
    from ..settings import download_fonts_dir
except:
    sys.path.append('../')
    from settings import download_fonts_dir

class CrawlerDriver(object):
    def __init__(self):
        # choose chrome driver
        os_platform = sys.platform
        self.driver_path = ''
        self.driver = None

        if os_platform.find('linux') != -1:
            self.driver_path = './drivers/linux_chromedriver'
        elif os_platform.find('darwin') != -1:
            self.driver_path = './drivers/mac_chromedriver'
        else:
            self.driver_path = 'null'

        if not os.path.exists(self.driver_path):
            raise Exception('ERROR: no chrome driver found!')

    def set_driver_opt(self, *args):
        for arg in args:
            if not type(arg) is str:
                raise Exception('ERROR: only string format options supported!')

        chrome_options = Options()
        for arg in args:
            chrome_options.add_argument(arg)

        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": download_fonts_dir,
            # "download.prompt_for_download": False,
            # "download.directory_upgrade": True,
            # "safebrowsing.enabled": True
            })

        self.driver = webdriver.Chrome(executable_path=(self.driver_path), \
                          chrome_options=chrome_options)

        
    def get_html(self, url, sleep_time=5):
        self.driver.get(url)
        time.sleep(sleep_time)
        return self.driver.page_source

    def download(self, url, sleep_time=5):
        self.driver.get(url)
        time.sleep(sleep_time)

    def get_cookie(self):
        return self.driver.get_cookies()

    def close_driver(self):
        self.driver.close()


CD = CrawlerDriver()
# CD.set_driver_opt('headless')
CD.set_driver_opt()

if __name__ == '__main__':
    # base_url = 'http://landchina.com/default.aspx?tabid=261&wmguid=20aae8dc-4a0c-4af5-aedf-cc153eb6efdf&p='
    # print CD.get_html(base_url)
    # base_url = 'https://baidu.com'
    # print CD.get_html(base_url)
    base_url = 'http://www.landchina.com/styles/fonts/pieXATBGyLsPEWSOUSu1wfcC3r3vM8aa.woff?fdipzone'
    a = CD.download(base_url, 20)
    print(a)
    print(CD.get_cookie())
    CD.close_driver()
