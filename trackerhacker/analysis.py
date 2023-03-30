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
                    total_ad_tracker_requests = sum(fqdn_info.values())
                    self.results[source_url][browser][fqdn] = {"ips": self._get_ips(fqdn), "ad_tracker_count": total_ad_tracker_requests}

    def _get_ips(self, fqdn: str) -> list:
        fqdn_ips = []
        answers = dns.resolver.resolve(fqdn, 'A')
        for a in answers:
            fqdn_ips.append(str(a))

        return fqdn_ips
    
    def get_results(self) -> dict:
        return self.results

    def do_whois_analysis(self) -> None:
        #TODO move whois data to new section of self.results, so there aren't duplicates
        whois_cache = {}
        for source_url, source_url_info in self.results.items():
            for browser, browser_info in source_url_info.items():
                for fqdn, _ in browser_info.items():
                    if fqdn in whois_cache.keys():
                        self._logger.debug("whois cache for %s" % fqdn)
                        self.results[source_url][browser][fqdn]["whois"] = whois_cache[fqdn]
                        continue

                    try:
                        self._logger.debug("Running whois for %s" % fqdn)
                        self.results[source_url][browser][fqdn]["whois"] = whois_cache[fqdn] = whois.whois(fqdn)
                    except whois.parser.PywhoisError as e:
                        self._logger.warning(e)
                    
    def do_server_location_analysis(self) -> None:
        geolocation_cache = {}
        for source_url, source_url_info in self.results.items():
            for browser, browser_info in source_url_info.items():
                for fqdn, _ in browser_info.items():
                    results = []
                    for ip in self.results[source_url][browser][fqdn]["ips"]:
                        if ip in geolocation_cache.keys():
                            self._logger.debug("Geolocation cache for %s" % ip)
                            results.append(geolocation_cache[ip])
                            continue

                        success = False
                        while not success:
                            try:
                                request_url = 'https://geolocation-db.com/jsonp/' + ip
                                response = requests.get(request_url)
                                result = response.content.decode()
                                result = result.split("(")[1].strip(")")
                                result = json.loads(result)
                                self._logger.debug(f"Geolocation for {ip}: {result}")
                                results.append(result)
                                success = True
                                geolocation_cache[ip] = result
                            except Exception:
                                self._logger.warning("Unable to geolocate '%s'. Trying again..." % ip)

                    self.results[source_url][browser][fqdn]["server_location"] = results