from enum import Enum
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

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

open_websites(["https://duckduckgo.com"], [WebBrowsers.FIREFOX])
