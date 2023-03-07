import asyncio
import os
import selenium
import threading
import time

from mitmproxy.tools import main
from mitmproxy.tools.dump import DumpMaster

import browsermanager
import webproxy


def collect_fqdns(logger, urls: list, browsers: list, proxy_ip: str="127.0.0.1", proxy_port: int=8080, request_timeout: int=5, headless: bool=False) -> dict:
    # results: each url contains dict of browsers, which contains list of fqdns where requests were made when loading url in browser
    results = {}

    webdrivers = browsermanager.WebDrivers(logger)
    for browser in browsers:
        if not webdrivers.download_driver(browser):
            return None

    os.environ["http_proxy"] = "http://%s:%d" % (proxy_ip, proxy_port)
    os.environ["https_proxy"] = "http://%s:%d" % (proxy_ip, proxy_port)
    os.environ["no_proxy"] = "localhost,127.0.0.1,::1"
    os.environ["HTTP_PROXY"] = "http://%s:%d" % (proxy_ip, proxy_port)
    os.environ["HTTPS_PROXY"] = "http://%s:%d" % (proxy_ip, proxy_port)
    os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"

    proxy = webproxy.Proxy(logger, request_timeout)
    logger.info("Starting proxy")
    # launch proxy in background
    t = threading.Thread(target=_start_proxy_launcher, args=(proxy, proxy_ip, proxy_port))
    t.start()

    for url in urls:
        results[url] = {}
        for browser in browsers:
            logger.info("Launching %s to open %s" % (browser.value, url))
            driver = webdrivers.get_driver(browser, proxy_ip=proxy_ip, proxy_port=proxy_port, headless=headless)
            if driver is None:
                continue

            time.sleep(2)
            proxy.collect_data()
            try:
                driver.get(url)
            except selenium.common.exceptions.WebDriverException:
                logger.error("Unable to connect to '%s'. This may be because\n\t- There is no internet connection\n\t- The browser has been closed\n\t- The URL is not valid" % url)
                try:
                    driver.close()
                except selenium.common.exceptions.WebDriverException:
                    pass
                
                continue

            # wait for the data to be collected
            while proxy.is_data_collection_in_progress():
                time.sleep(2)

            logger.debug("closing webpage")
            try:
                driver.close()
            except selenium.common.exceptions.WebDriverException:
                pass

            logger.debug("RESULTS:", proxy.get_fqdns())
            results[url][browser] = proxy.get_fqdns()


    logger.debug("shutting down proxy")
    proxy.shutdown_proxy()
    return results


def _start_proxy_launcher(proxy: webproxy.Proxy, host: str, port: int) -> None:
    asyncio.run(_start_proxy(proxy, host, port))


async def _start_proxy(proxy: webproxy.Proxy, host: str, port: int):
    opts = main.options.Options(listen_host=host, listen_port=port)
    master = DumpMaster(options=opts, with_termlog=False, with_dumper=False)
    master.addons.add(proxy)
    await master.run()
    return master


if __name__ == "__main__":
    collect_fqdns(["https://google.com"], [browsermanager.WebBrowsers.EDGE, browsermanager.WebBrowsers.CHROME, browsermanager.WebBrowsers.BRAVE, browsermanager.WebBrowsers.FIREFOX])

