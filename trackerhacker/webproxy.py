import threading
import time

from logging import Logger

from mitmproxy import ctx, http

#Proxy class
class Proxy:
    
    #Self initialization of all data attributes during the run
    def __init__(self, logger: Logger, request_timeout: int=5, absolute_timeout: int=300) -> None:
        self._logger = logger
        self.fqdns = {}
        self.request_made_since_last_check = True
        self.data_collection_in_progress = False
        self.request_timeout = request_timeout
        self.absolute_timeout = absolute_timeout

    #Method to initiate data collection thread
    def collect_data(self) -> None:
        self.fqdns = {}
        self.request_made_since_last_check = True
        self.data_collection_in_progress = True

        t = threading.Thread(target=self.check_timeout, args=(self.request_timeout, self.absolute_timeout))
        t.start()

    #Method to determine timeout of proxy query
    def check_timeout(self, request_timeout: int, absolute_timeout: int) -> None:
        start_time = time.time()
        while self.request_made_since_last_check:
            if time.time() - start_time > absolute_timeout:
                break

            self.request_made_since_last_check = False
            time.sleep(request_timeout)

        self._logger.debug("timeout reached")
        self.data_collection_in_progress = False

    #method to track current status of data collection
    def is_data_collection_in_progress(self) -> bool:
        return self.data_collection_in_progress

    #Method to shut down the proxy
    def shutdown_proxy(self) -> None:
        try:
            ctx.master.shutdown()
        except Exception as e:
            self._logger.warning(e)

    #Method that returns collected fqdsn
    def get_fqdns(self) -> dict[str, dict[str, int]]:
        return self.fqdns

    #Request method
    def request(self, flow: http.HTTPFlow) -> None:
        if self.data_collection_in_progress:
            self.request_made_since_last_check = True
            fqdn = flow.request.host
            url = "%s://%s%s" % (flow.request.scheme, fqdn, flow.request.path)
            if fqdn not in self.fqdns:
                self.fqdns[fqdn] = {}

            if url in self.fqdns[fqdn]:
                self.fqdns[fqdn][url] += 1
            else:
                self.fqdns[fqdn][url] = 1

            self._logger.debug(fqdn)
