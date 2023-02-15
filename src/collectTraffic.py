from enum import Enum
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os
import asyncio

from mitmproxy import options
from mitmproxy.tools.dump import DumpMaster


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
                fp = webdriver.FirefoxProfile()

                fp.set_preference("network.proxy.type", 1)
                fp.set_preference("network.proxy.http", "127.0.0.1")
                fp.set_preference("network.proxy.http_port", 8080)
                fp.set_preference("network.proxy.ssl", "127.0.0.1")
                fp.set_preference("network.proxy.ssl_port", 8080)
                fp.update_preferences()

                opts = webdriver.FirefoxOptions()
                opts.set_profile(fp)

                #finish including firefox object
                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

            asyncio.run(start_proxy('127.0.0.1', 8080))
            sleep(2)
            driver.get(url)


async def start_proxy(host, port):
    opts = options.Options(listen_host=host, listen_port=port)

    master = DumpMaster(
        opts,
        with_termlog=False,
        with_dumper=False,
    )
    master.addons.add(Proxy())

    await master.run()
    return master


open_websites(["https://duckduckgo.com"], [WebBrowsers.FIREFOX])

