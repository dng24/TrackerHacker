import dns.resolver
import json
import requests
import whois

class Analysis:
    def __init__(self, logger, ad_tracker_data_dict: dict) -> None:
        self._logger = logger
        self.results = {}
        for source_url, source_url_info in ad_tracker_data_dict.items():
            self.results[source_url] = {}
            for browser, browser_info in source_url_info.items():
                self.results[source_url][browser] = {}
                for fqdn, fqdn_info in browser_info.items():
                    self.results[source_url][browser][fqdn] = {"ips": self._get_ips(fqdn)}


    def _get_ips(self, fqdn: str) -> list:
        fqdn_ips = []
        answers = dns.resolver.resolve(fqdn, 'A')
        for a in answers:
            fqdn_ips.append(str(a))

        return fqdn_ips

    
    def get_results(self) -> dict:
        return self.results


    def do_whois_analysis(self) -> None:
        for source_url, source_url_info in self.results.items():
            for browser, browser_info in source_url_info.items():
                for fqdn, fqdn_info in browser_info.items():
                    whois_results = None
                    self.results[source_url][browser][fqdn]["whois"] = whois.whois(fqdn)
                    

    def do_server_location_analysis(self) -> None:
        for source_url, source_url_info in self.results.items():
            for browser, browser_info in source_url_info.items():
                for fqdn, fqdn_info in browser_info.items():
                    server_location_results = self._geolocate(self.results[source_url][browser][fqdn]["ips"])
                    self.results[source_url][browser][fqdn]["server_location"] = server_location_results


    def _geolocate(self, ips: list) -> list:
        results = []
        for ip in ips:
            print(ip, type(ip))
            request_url = 'https://geolocation-db.com/jsonp/' + ip
            print(request_url)
            response = requests.get(request_url)
            result = response.content.decode()
            result = result.split("(")[1].strip(")")
            result = json.loads(result)
            print(f"Geolocation for {ip}: \n\n  {result}")
            results.append(result)

        return results