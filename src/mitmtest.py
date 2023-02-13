from mitmproxy import http
from mitmproxy import ctx

class ChangeHTTPCode:
    filter = "google.com"

    def response(self, flow: http.HTTPFlow) -> None:
        if (self.filter in flow.request.pretty_url):
            flow.response.status_code = 504

addons = [ChangeHTTPCode]