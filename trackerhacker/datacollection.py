import asyncio
import os
import threading
import time

from logging import Logger
from mitmproxy.tools import main
from mitmproxy.tools.dump import DumpMaster
from selenium.common.exceptions import WebDriverException

from trackerhacker.browsermanager import WebBrowsers
from trackerhacker.browsermanager import WebDrivers
from trackerhacker.webproxy import Proxy


#Collects all of the data and aggregates it into a data store
def collect_request_urls(logger: Logger, urls: list[str], browsers: list[WebBrowsers], proxy_ip: str="127.0.0.1", proxy_port: int=8080, request_timeout: int=5, absolute_timeout: int=300, headless: bool=False) -> dict[str, dict[str, dict[str, dict[str, int]]]]:
    # results: each url contains dict of browsers, which contains dict of fqdns, which contains dict of full request url to number request made to that url
    results = {}

    webdrivers = WebDrivers(logger)
    for browser in browsers:
        if not webdrivers.download_driver(browser):
            return None

    #Sets environmental os variables
    os.environ["http_proxy"] = "http://%s:%d" % (proxy_ip, proxy_port)
    os.environ["https_proxy"] = "http://%s:%d" % (proxy_ip, proxy_port)
    os.environ["no_proxy"] = "localhost,127.0.0.1,::1"
    os.environ["HTTP_PROXY"] = "http://%s:%d" % (proxy_ip, proxy_port)
    os.environ["HTTPS_PROXY"] = "http://%s:%d" % (proxy_ip, proxy_port)
    os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"

    logger.info("Starting proxy")

    proxy = Proxy(logger, request_timeout, absolute_timeout)
    try:
        # launch proxy in background
        t = threading.Thread(target=_start_proxy_launcher, args=(proxy, proxy_ip, proxy_port))
        t.start()

        total_urls = len(urls) * len(browsers)
        progress = 1
        for url in urls:
            results[url] = {}
            for browser in browsers:
                logger.info("Launching %s to open %s [%d/%d]" % (browser.value, url, progress, total_urls))
                progress += 1
                driver = webdrivers.get_driver(browser, proxy_ip=proxy_ip, proxy_port=proxy_port, headless=headless)
                if driver is None:
                    continue

                time.sleep(2)
                proxy.collect_data()
                try:
                    driver.get(url)
                    driver.set_page_load_timeout(absolute_timeout)
                except WebDriverException:
                    logger.error("Unable to connect to '%s'. This may be because\n\t- There is no internet connection\n\t- The browser has been closed\n\t- The URL is not valid" % url)
                    try:
                        driver.quit()
                    except WebDriverException:
                        pass
                    
                    continue

                # wait for the data to be collected
                while proxy.is_data_collection_in_progress():
                    time.sleep(2)

                logger.debug("closing webpage")
                try:
                    driver.quit()
                except WebDriverException:
                    pass

                fqdns = proxy.get_fqdns()
                if len(fqdns) == 0:
                    logger.warning("'%s' on %s had no requests. Excluding from results....." % (url, browser.value))
                else:
                    results[url][browser.value] = fqdns

            if len(results[url]) == 0:
                logger.warning("'%s' had no requests. Excluding from results....." % url)
                del results[url]

        logger.debug("shutting down proxy")
        proxy.shutdown_proxy()
    except:
        proxy.shutdown_proxy()
        raise

    os.environ["http_proxy"] = ""
    os.environ["https_proxy"] = ""
    os.environ["no_proxy"] = ""
    os.environ["HTTP_PROXY"] = ""
    os.environ["HTTPS_PROXY"] = ""
    os.environ["NO_PROXY"] = ""
    return results

#Initiaties the asyncio proxy launcher
def _start_proxy_launcher(proxy: Proxy, host: str, port: int) -> None:
    asyncio.run(_start_proxy(proxy, host, port))

#Starts the web proxy
async def _start_proxy(proxy: Proxy, host: str, port: int) -> DumpMaster:
    opts = main.options.Options(listen_host=host, listen_port=port)
    master = DumpMaster(options=opts, with_termlog=False, with_dumper=False)
    master.addons.add(proxy)
    await master.run()
    return master
