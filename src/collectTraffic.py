from enum import Enum
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os



class WebBrowsers(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"

def open_websites(urls, browsers):
    for browser in browsers:
        if browser == WebBrowsers.CHROME:
            driver = webdriver.Chrome()
        elif browser == WebBrowsers.FIREFOX:
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

        for url in urls:
            driver.get(url)

def load_proxy(file):
    os.system(f"mitmdump -s {}", file)


open_websites(["https://duckduckgo.com"], [WebBrowsers.FIREFOX])

