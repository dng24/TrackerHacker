from enum import Enum
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

import os
import asyncio
import threading
import time

from mitmproxy.tools import main
from mitmproxy.tools.dump import DumpMaster

import proxycollect

class WebBrowsers(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"

def open_websites(urls, browsers):
    for url in urls:
        for browser in browsers:
            if browser == WebBrowsers.CHROME:
                driver = webdriver.Chrome()
            elif browser == WebBrowsers.FIREFOX:
                # setup firefox proxy
                opts = webdriver.FirefoxOptions()
                opts.set_preference("network.proxy.type", 1)
                opts.set_preference("network.proxy.http", "127.0.0.1")
                opts.set_preference("network.proxy.http_port", 8080)
                opts.set_preference("network.proxy.ssl", "127.0.0.1")
                opts.set_preference("network.proxy.ssl_port", 8080)
                driver = webdriver.Firefox(options=opts, service=FirefoxService(GeckoDriverManager().install()))

            # launch proxy in background
            t = threading.Thread(target=start_proxy_launcher, args=('127.0.0.1', 8080))
            t.start()

            # wait for proxy to boot up
            time.sleep(2)
            # go to URL with selenium
            driver.get(url)


def start_proxy_launcher(host, port):
    asyncio.run(start_proxy(host, port))


async def start_proxy(host, port):
    opts = main.options.Options(listen_host=host, listen_port=port)
    master = DumpMaster(options=opts, with_termlog=False, with_dumper=False)
    master.addons.add(proxycollect.MyProxy())
    await master.run()
    return master


open_websites(["https://cnn.com"], [WebBrowsers.FIREFOX])

