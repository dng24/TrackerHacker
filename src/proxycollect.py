import threading
import time

from mitmproxy import ctx, http


class Proxy:
    
    def __init__(self, request_timeout: int=5) -> None:
        self.fqdns = {}
        self.request_made_since_last_check = True
        self.shutdown = False
        #threading.Thread(target=self._check_timeout, args=(request_timeout,))
        print("init")


    def _check_timeout(self, request_timeout: int) -> None:
        while self.request_made_since_last_check:
            self.request_made_since_last_check = False
            time.sleep(request_timeout)

        print("timeout reached")
        self.shutdown = True


    def should_shutdown(self) -> bool:
        return self.shutdown


    def shutdown(self) -> None:
        ctx.master.shutdown()


    def get_fqdns(self) -> dict:
        return self.fqdns


    def request(self, flow: http.HTTPFlow) -> None:
        self.request_made_since_last_check = True
        fqdn = flow.request.host
        if fqdn in self.fqdns:
            self.fqdns[fqdn] += 1
        else:
            self.fqdns[fqdn] = 1

        print(flow.request.host)
        print("aaa")
