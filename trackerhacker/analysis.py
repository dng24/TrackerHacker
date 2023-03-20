

class Analysis:
    def __init__(self, logger, ad_tracker_data_dict: dict) -> None:
        self._logger = logger
        self.results = {}
        for source_url, source_url_info in ad_tracker_data_dict.items():
            self.results[source_url] = {}
            for browser, browser_info in source_url_info.items():
                self.results[source_url][browser] = {}
                for fqdn, fqdn_info in browser_info.items():
                    self.results[source_url][browser][fqdn] = {}


    def get_results(self) -> dict:
        return self.results


    def do_whois_analysis(self) -> None:
        for source_url, source_url_info in collected_request_urls.items():
            for browser, browser_info in source_url_info.items():
                for fqdn, fqdn_info in browser_info.items():
                    whois_results = None
                    self.results[source_url][browser][fqdn]["whois"] = whois_results
                    

    def do_server_location_analysis(self) -> None:
        for source_url, source_url_info in collected_request_urls.items():
            for browser, browser_info in source_url_info.items():
                for fqdn, fqdn_info in browser_info.items():
                    server_location_results = None
                    self.results[source_url][browser][fqdn]["server_location"] = server_location_results

