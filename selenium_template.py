# coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from fake_useragent import UserAgent
from collections import defaultdict
import random
import time
import os

# =============================================================================
# 
# =============================================================================

def scroll_shim(passed_in_driver, object):
    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    scroll_nav_out_of_way = 'window.scrollBy(0, {});'.format(random.randint(-350,-250))
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)
    
def scroll_shim(passed_in_driver, object):
    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)

def click_locxy(dr, x, y, left_click=True):
    if left_click:
        ActionChains(dr).move_by_offset(x, y).click().perform()
    else:
        ActionChains(dr).move_by_offset(x, y).context_click().perform()
    ActionChains(dr).move_by_offset(-x, -y).perform()  # 將滑鼠位置恢復到移動前

# =============================================================================
# 
# =============================================================================

yearFrom = 2017
yearTo   = 2021
start_url = r"https://www.spiedigitallibrary.org/conference-proceedings-of-spie/browse/SPIE-Advanced-Lithography"
web_url   = r"https://www.spiedigitallibrary.org"

download_dir = os.sep.join([os.getcwd(),"SPIE"])
mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", download_dir)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
fp.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
fp.set_preference("pdfjs.disabled", True)

browser = webdriver.Firefox(firefox_profile=fp)
browser.maximize_window()
browser.get(start_url)

recordurl = defaultdict(lambda : dict())
for year in range(yearFrom, yearTo+1):
    yearLink_key = "//div[@id='InnerYearDivspie-advanced-lithography{0}']".format(year)
    yearLinks = browser.find_elements_by_xpath(yearLink_key)
    if len(yearLinks)==0:
        print(f"There is no {year} infomation!")
        continue
    
    scroll_shim(browser, yearLinks[0])
    ActionChains(browser).move_to_element(yearLinks[0]).perform()
    if yearLinks[0].is_displayed():
        yearLinks[0].click()
        items = browser.find_elements_by_xpath("//div[@id='InnerYearItemspie-advanced-lithography{0}']//a[contains(@href,'')]".format(year))
        for item in items:
            if not item.text.isnumeric():
                recordurl[year][item.text] = item.get_attribute("href")
                
for year, item1 in recordurl.items():
    for className, url in item1.items():
        browser.get(url)
        break
    break
