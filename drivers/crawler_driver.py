# -*- coding: utf-8 -*-

import sys
import os
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
try:
    from ..settings import base_dir, download_fonts_dir
except:
    current_dir = os.path.dirname(__file__)
    sys.path.append(os.path.join(current_dir, '../'))
    from settings import base_dir, download_fonts_dir

class CrawlerDriver(object):
    def __init__(self, headless=True):
        # choose chrome driver
        os_platform = sys.platform
        self.driver_path = ''
        self.driver = None

        if os_platform.find('linux') != -1:
            self.driver_path = os.path.join(base_dir, 'drivers/linux_chromedriver')
        elif os_platform.find('darwin') != -1:
            self.driver_path = os.path.join(base_dir, 'drivers/mac_chromedriver')
        else:
            self.driver_path = 'null'

        if not os.path.exists(self.driver_path):
            raise Exception('ERROR: no chrome driver found!')

        self.set_driver_opt(headless=headless)

        if headless:
            self.enable_headless_download_feature()

    def set_driver_opt(self, headless=True):
        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": download_fonts_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
            "safebrowsing.disable_download_protection": True
        })

        if headless == True:
            chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(executable_path=(self.driver_path), \
                                       chrome_options=chrome_options)

    def enable_headless_download_feature(self):
        """
        there is currently a "feature" in chrome where
        headless does not allow file download: https://bugs.chromium.org/p/chromium/issues/detail?id=696481#c80
        This method is a hacky work-around until the official chromedriver support for this.
        Requires chrome version 62.0.3196.0 or above.
        """

        # add missing support for chrome "send_command"  to selenium webdriver
        self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_fonts_dir}}
        command_result = self.driver.execute("send_command", params)
        print('Response from browser:')
        for k in command_result:
            print('%s: %s' % (k, command_result[k]))

    def get_html(self, url, sleep_time=5):
        self.driver.get(url)
        time.sleep(sleep_time)
        return self.driver.page_source

    def download(self, url, sleep_time=5):
        self.driver.get(url)
        time.sleep(sleep_time)
        start_pos = url.rfind('/') + 1
        end_pos = url.rfind('?')
        if start_pos == -1 or end_pos == -1:
            file_list = os.listdir(download_fonts_dir)
            filename = ''
            for tmp in file_list:
                if url.find(tmp) != -1:
                    filename = tmp
                    break
        else:
            filename = url[start_pos:end_pos]

        return os.path.join(download_fonts_dir, filename)

    def get_cookie(self):
        return self.driver.get_cookies()

    def close_driver(self):
        self.driver.close()


CD = CrawlerDriver()

if __name__ == '__main__':
    # base_url = 'http://landchina.com/default.aspx?tabid=261&wmguid=20aae8dc-4a0c-4af5-aedf-cc153eb6efdf&p='
    # print CD.get_html(base_url)
    # base_url = 'https://baidu.com'
    # print CD.get_html(base_url)
    base_url = 'http://www.landchina.com/styles/fonts/pieXATBGyLsPEWSOUSu1wfcC3r3vM8aa.woff?fdipzone'
    a = CD.download(base_url)
    print(a)
    print(CD.get_cookie())
    CD.close_driver()
