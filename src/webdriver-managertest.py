import os

import requests
from requests import Response

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.download_manager import WDMDownloadManager
from webdriver_manager.core.http import HttpClient
from webdriver_manager.core.logger import log
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

class CustomHttpClient(HttpClient):

    def get(self, url, params=None, **kwargs) -> Response:
        """
        Add you own logic here like session or proxy etc.
        """
        log("The call will be done with custom HTTP client")
        result = requests.get(url, params, **kwargs)
        print(url)
        return result


def test_custom_client():
    http_client = CustomHttpClient()
    options = Options()
    # options.binary_location = r'C:\Users\treba\Documents\GitHub\TrackerHacker\drivers\.wdm\drivers\chromedriver\win32\110.0.5481\chromedriver.exe'
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.proxy = http_client
    # download_manager = WDMDownloadManager(http_client)
    # path = ChromeDriverManager(download_manager=download_manager, path=r'./drivers/').install()
    # assert os.path.exists(path)
    # print(path)
    # print(http_client.get('https://www.google.com'))
    print(os.getcwd())
    driver = webdriver.Chrome(chrome_options = options, service=ChromeService(r'C:\Users\treba\Documents\GitHub\TrackerHacker\drivers\.wdm\drivers\chromedriver\win32\110.0.5481\chromedriver.exe'))
    driver.get("https://www.google.com")

test_custom_client()