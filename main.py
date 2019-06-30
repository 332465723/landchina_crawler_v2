# -*- coding: utf-8 -*-

import sys
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# choose chrome driver
os_platform = sys.platform
driver_path = ''
if os_platform.find('linux') != -1:
    driver_path = './drivers/linux_chromedriver'
elif os_platform.find('darwin') != -1:
    driver_path = './drivers/mac_chromedriver'
else:
    driver_path = 'null'

if not os.path.exists(driver_path):
    print('ERROR: no chrome driver found!')
    exit(0)

# config
chrome_options = Options()
chrome_options.add_argument("headless")
base_url = 'http://landchina.com/default.aspx?tabid=261&wmguid=20aae8dc-4a0c-4af5-aedf-cc153eb6efdf&p='

driver = webdriver.Chrome(executable_path=(driver_path), \
                          chrome_options=chrome_options)

driver.get(base_url)
time.sleep(5)
print(driver.page_source)
driver.close()

