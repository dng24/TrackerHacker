import dns.resolver
import logging
import json
import requests
import whois
import pandas as pd
import ipaddress
import pickle
import os
from cidr_trie import PatriciaTrie

class Analysis:
    def __init__(self, logger, ad_tracker_data_dict: dict, root_directory: str, initial_results={}) -> None:
        self._logger = logger
        self.root_directory = root_directory
        self.results = initial_results
        if not initial_results:
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
        dbip_df = pd.read_csv(os.path.join(self.root_directory, 'res/geolite_combined_filtered.csv'))
        dbip_df['IPv4'] = dbip_df.IPv4.astype(str)
        dbip_df.set_index('IPv4', inplace=True)
        pickle_file = open(os.path.join(self.root_directory, 'res/cidr_trie_pickle.pkl'), 'rb')
        cidr_trie = pickle.load(pickle_file)

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

                        """
                        range_found = False
                        ip_ipaddress = ipaddress.ip_address(ip)
                        for cidr in dbip_df.index.values.tolist():
                            cidr_network = ipaddress.ip_network(cidr)
                            if ip_ipaddress in cidr_network:
                                result = dbip_df.loc[cidr]
                                self._logger.debug(f"GeoliteDB geolocation for {ip}: {result}")
                                results.append(result)
                                geolocation_cache[ip] = result
                                range_found = True
                                break
                        """

                        cidr_trie_find_result = cidr_trie.find_all(ip)
                        if cidr_trie_find_result:
                            result_series = dbip_df.loc[cidr_trie_find_result[0][0]]
                            result = result_series.to_dict()
                            result.update({'IPv4': ip})
                            self._logger.debug(f"GeoliteDB geolocation for {ip}: {result}")
                            results.append(result)
                            geolocation_cache[ip] = result
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

    def do_server_location_analysis_db(self) -> None:
        dbip_df = pd.read_csv(os.path.join(self.root_directory, 'res/geolite_combined_filtered.csv'))
        dbip_df.set_index('IPv4')
        for source_url, source_url_info in self.results.items():
            for browser, browser_info in source_url_info.items():
                for fqdn, _ in browser_info.items():
                    results = []
                    for ip in self.results[source_url][browser][fqdn]["ips"]:
                        range_found = False
                        ip_ipaddress = ipaddress.ip_address(ip)
                        for cidr in dbip_df['IPv4']:
                            if ip_ipaddress in ipaddress.ip_network(cidr):
                                results.append(dbip_df.iloc[[cidr]])
                                range_found = True
                        
                        if not range_found:
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
                                except Exception:
                                    self._logger.warning("Unable to geolocate '%s'. Trying again..." % ip)


if __name__ == "__main__":
    LOGGER_FORMAT = "[TRACKER HACKER] %(levelname)-8s: %(message)s"
    LOGGER_LEVEL = logging.DEBUG
    logging.basicConfig(format=LOGGER_FORMAT)
    logger = logging.getLogger("tracker_hacker")
    logger.setLevel(LOGGER_LEVEL)

    parsed_data_f = open('../tests/test_data/parsed_cnn_data.txt', 'r')
    parsed_data = json.load(parsed_data_f)
    parsed_data_f.close()
    air_f = open('../tests/test_data/cnn_analysis_initial_results.json', 'r')
    air = json.load(air_f)
    air_f.close()
    a = Analysis(logger, parsed_data, initial_results=air)

    a.do_server_location_analysis()
    print(a.get_results())