import asyncio
import selenium
import threading
import time

from mitmproxy.tools import main
from mitmproxy.tools.dump import DumpMaster
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

import webproxy
from browsers import WebBrowsers


# results: each url contains dict of browsers, which contains list of fqdns where requests were made when loading url in browser
results = {}


def collect_fqdns(urls: list, browsers: list, request_timeout: int=5) -> dict:
    proxy = webproxy.Proxy(request_timeout)
    print("Starting proxy")
    # launch proxy in background
    t = threading.Thread(target=_start_proxy_launcher, args=(proxy, '127.0.0.1', 8080))
    t.start()

    for url in urls:
        results[url] = {}
        for browser in browsers:
            if browser == WebBrowsers.CHROME:
                try:
                    driver = webdriver.Chrome()
                except selenium.common.exceptions.WebDriverException:
                    print("ur chrome is broke or missing")
                    continue
            elif browser == WebBrowsers.FIREFOX:
                # setup firefox proxy
                opts = webdriver.FirefoxOptions()
                opts.set_preference("network.proxy.type", 1)
                opts.set_preference("network.proxy.http", "127.0.0.1")
                opts.set_preference("network.proxy.http_port", 8080)
                opts.set_preference("network.proxy.ssl", "127.0.0.1")
                opts.set_preference("network.proxy.ssl_port", 8080)
                try:
                    #TODO get this so it only installs first time
                    driver = webdriver.Firefox(options=opts, service=FirefoxService(GeckoDriverManager().install()))
                except selenium.common.exceptions.WebDriverException:
                    print("ur firefox is broke or missing")
                    continue

            time.sleep(2)
            proxy.collect_data()
            print("launching webpage")
            try:
                driver.get(url)
            except selenium.common.exceptions.WebDriverException:
                print("Unable to connect to %s" % url)
                driver.close()
                continue

            # wait for the data to be collected
            while proxy.is_data_collection_in_progress():
                time.sleep(2)

            print("closing webpage")
            driver.close()

            print("RESULTS:", proxy.get_fqdns())
            results[url][browser] = proxy.get_fqdns()


    print("shutting down proxy")
    proxy.shutdown_proxy()


def _start_proxy_launcher(proxy: webproxy.Proxy, host: str, port: int) -> None:
    asyncio.run(_start_proxy(proxy, host, port))


async def _start_proxy(proxy: webproxy.Proxy, host: str, port: int):
    opts = main.options.Options(listen_host=host, listen_port=port)
    master = DumpMaster(options=opts, with_termlog=False, with_dumper=False)
    master.addons.add(proxy)
    await master.run()
    return master


if __name__ == "__main__":
    collect_fqdns(["https://cnn.com"], [WebBrowsers.FIREFOX])

