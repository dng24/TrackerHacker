#! /bin/env/python3

from mitmproxy import ctx, http
import time

class MyProxy:

    def request(self, flow: http.HTTPFlow):
        print(flow.request.host)
