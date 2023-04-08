import threading
import time

from mitmproxy import ctx, http


class Proxy:
    
    def __init__(self, logger, request_timeout: int=5, absolute_timeout: int=300) -> None:
        self._logger = logger
        self.fqdns = {}
        self.request_made_since_last_check = True
        self.data_collection_in_progress = False
        self.request_timeout = request_timeout
        self.absolute_timeout = absolute_timeout


    def collect_data(self) -> None:
        self.fqdns = {}
        self.request_made_since_last_check = True
        self.data_collection_in_progress = True

        t = threading.Thread(target=self.check_timeout, args=(self.request_timeout, self.absolute_timeout))
        t.start()


    def check_timeout(self, request_timeout: int, absolute_timeout: int) -> None:
        start_time = time.time()
        while self.request_made_since_last_check:
            if time.time() - start_time > absolute_timeout:
                break
            
            self.request_made_since_last_check = False
            time.sleep(request_timeout)

        self._logger.debug("timeout reached")
        self.data_collection_in_progress = False


    def is_data_collection_in_progress(self) -> bool:
        return self.data_collection_in_progress


    def shutdown_proxy(self) -> None:
        ctx.master.shutdown()


    def get_fqdns(self) -> dict:
        return self.fqdns


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
