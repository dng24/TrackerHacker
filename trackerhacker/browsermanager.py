import os
import selenium
import sys

from enum import Enum
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.microsoft import EdgeChromiumDriverManager


DEFAULT_BRAVE_LINUX_PATH = "/usr/bin/brave-browser"
DEFAULT_BRAVE_WIN_PATH = "C:/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe"
DEFAULT_BRAVE_WIN_64_PATH = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
DEFAULT_BRAVE_MAC_PATH = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"


class WebBrowsers(Enum):
    CHROME = "Chrome"
    FIREFOX = "Firefox"
    EDGE = "Edge"
    BRAVE = "Brave"


class WebDrivers:
    def __init__(self, logger) -> None:
        self._logger = logger
        self.driver_paths: str = {}

    def download_driver(self, browser: WebBrowsers) -> bool:
        try:
            if browser == WebBrowsers.CHROME:
                self.driver_paths[WebBrowsers.CHROME] = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            elif browser == WebBrowsers.FIREFOX:
                self.driver_paths[WebBrowsers.FIREFOX] = GeckoDriverManager().install()
            elif browser == WebBrowsers.EDGE:
                self.driver_paths[WebBrowsers.EDGE] = EdgeChromiumDriverManager().install()
            elif browser == WebBrowsers.BRAVE:
                self.driver_paths[WebBrowsers.BRAVE] = ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()
            else:
                raise("Browser not supported: %s" % browser)
        except Exception:
            self._logger.error("Unable to download %s driver. Check your Internet connection." % browser.value)
            return False

        return True
    
    def get_driver(self, browser: WebBrowsers, browser_path: str=None, proxy_ip: str="127.0.0.1", proxy_port: int=8080, headless: bool=False) -> webdriver:
        driver = None
        try:
            if browser == WebBrowsers.CHROME:
                opts = webdriver.ChromeOptions()
                if headless:
                    opts.headless = True
                opts.add_argument("--proxy-server=http://%s:%d" % (proxy_ip, proxy_port))
                if browser_path is not None:
                    opts.binary_location = browser_path

                driver = webdriver.Chrome(service=ChromiumService(self.driver_paths[WebBrowsers.CHROME]), chrome_options=opts)
            elif browser == WebBrowsers.FIREFOX:
                # setup firefox proxy
                opts = webdriver.FirefoxOptions()
                if headless:
                    opts.headless = True
                opts.set_preference("network.proxy.type", 1)
                opts.set_preference("network.proxy.http", proxy_ip)
                opts.set_preference("network.proxy.http_port", proxy_port)
                opts.set_preference("network.proxy.ssl", proxy_ip)
                opts.set_preference("network.proxy.ssl_port", proxy_port)
                if browser_path is not None:
                    opts.binary_location = browser_path

                driver = webdriver.Firefox(options=opts, service=FirefoxService((self.driver_paths[WebBrowsers.FIREFOX])))
            elif browser == WebBrowsers.EDGE:
                opts = webdriver.EdgeOptions()
                if headless:
                    opts.headless = True
                opts.add_argument("--proxy-server=http://%s:%d" % (proxy_ip, proxy_port))
                if browser_path is not None:
                    opts.binary_location = browser_path
                
                driver = webdriver.Edge(service=EdgeService(self.driver_paths[WebBrowsers.EDGE]), options=opts)
            elif browser == WebBrowsers.BRAVE:
                opts = webdriver.ChromeOptions()
                if headless:
                    opts.headless = True
                opts.add_argument("--proxy-server=http://%s:%d" % (proxy_ip, proxy_port))
                if browser_path is not None:
                    opts.binary_location = browser_path
                if sys.platform.startswith("linux"):
                    opts.binary_location = DEFAULT_BRAVE_LINUX_PATH
                elif sys.platform.startswith("win32") and os.path.exists(DEFAULT_BRAVE_WIN_PATH):
                    opts.binary_location = DEFAULT_BRAVE_WIN_PATH
                elif sys.platform.startswith("win32") and os.path.exists(DEFAULT_BRAVE_WIN_64_PATH):
                    opts.binary_location = DEFAULT_BRAVE_WIN_64_PATH
                elif sys.platform.startswith("darwin"):
                    opts.binary_location = DEFAULT_BRAVE_MAC_PATH
                else:
                    self._logger.error("Unable to find Brave; please pass in the path to Brave.")
                    return driver

                driver = webdriver.Chrome(service=ChromiumService(self.driver_paths[WebBrowsers.BRAVE]), chrome_options=opts)
        except selenium.common.exceptions.WebDriverException:
            self._logger.error("Unable to open %s. Make sure:\n\t- You are connected to the Internet\n\t- %s is installed\n\t- %s is updated to the latest version\nAlternatively, try passing in the path to %s." % (browser.value, browser.value, browser.value, browser.value))

        return driver