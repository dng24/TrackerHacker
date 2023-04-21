import json
import numpy as np
import os
import pandas as pd
import pickle
import requests
import whois

from dns import exception, resolver
from logging import Logger
from whois import WhoisEntry


#Analysis class for use in analyzin collected web traffic to sift out ads and trackers 
class Analysis:
    
    #Initialization method
    def __init__(self, logger: Logger, ad_tracker_data_dict: dict[str, dict[str, dict[str, dict[str, int]]]], root_directory: str) -> None:
        self._logger = logger
        self.root_directory = root_directory
        self.results: dict[str, dict[str, dict[str, dict[str, list[str] | int | WhoisEntry | list[dict[str, str | None]]]]]] = {}
        for source_url, source_url_info in ad_tracker_data_dict.items():
            self.results[source_url] = {}
            for browser, browser_info in source_url_info.items():
                self.results[source_url][browser] = {}
                for fqdn, fqdn_info in browser_info.items():
                    total_ad_tracker_requests = sum(fqdn_info.values())
                    self.results[source_url][browser][fqdn] = {"ips": self._get_ips(fqdn), "ad_tracker_count": total_ad_tracker_requests}

    #Collects the ips of all collected fqdns
    def _get_ips(self, fqdn: str) -> list[str]:
        fqdn_ips = []
        tries = 0
        while True:
            try:
                answers = resolver.resolve(fqdn, 'A')
                for a in answers:
                    fqdn_ips.append(str(a))
                
                break
            except resolver.LifetimeTimeout:
                if tries > 4:
                    self._logger.warning("Unable to resolve '%s'" % fqdn)
                    break
                else:
                    tries += 1
            except exception.DNSException:
                self._logger.warning("Unable to resolve '%s'" % fqdn)
                break

        return fqdn_ips
    
    #Returns the result attribute of the analysis object
    def get_results(self) -> dict[str, dict[str, dict[str, dict[str, list[str] | int | WhoisEntry | list[dict[str, str | None]]]]]]:
        return self.results

    #Perfoms the whois analysis on collected fqdns
    def do_whois_analysis(self) -> None:
        whois_cache = {}
        #Iterates through the collected data of urls and performs a whois query on each item, storing the results in a custom data store
        for source_url, source_url_info in self.results.items():
            for browser, browser_info in source_url_info.items():
                for fqdn, _ in browser_info.items():
                    #Determinies if the item is cached and the program has already performed a whois on it, in which case it references the cache for improved time efficiency
                    if fqdn in whois_cache.keys():
                        self._logger.debug("whois cache for %s" % fqdn)
                        self.results[source_url][browser][fqdn]["whois"] = whois_cache[fqdn]
                        continue

                    try:
                        self._logger.debug("Running whois for %s" % fqdn)
                        self.results[source_url][browser][fqdn]["whois"] = whois_cache[fqdn] = whois.whois(fqdn)
                    except whois.parser.PywhoisError as e:
                        self._logger.warning(e)
                    
    #Performs the server location analysis
    def do_server_location_analysis(self) -> None:
        #Collects data from the geolit daatabase of location information and stores it for use by the program
        dbip_df = pd.read_csv(os.path.join(self.root_directory, 'res/geolite_combined_filtered.csv'))
        dbip_df['IPv4'] = dbip_df.IPv4.astype(str)
        dbip_df.set_index('IPv4', inplace=True)
        pickle_file = open(os.path.join(self.root_directory, 'res/cidr_trie_pickle.pkl'), 'rb')
        cidr_trie = pickle.load(pickle_file)

        geolocation_cache = {}
        #Iterate through the fqdns collected by the program and performs location lookup on each item
        for source_url, source_url_info in self.results.items():
            for browser, browser_info in source_url_info.items():
                for fqdn, _ in browser_info.items():
                    results = []
                    for ip in self.results[source_url][browser][fqdn]["ips"]:
                        #Determines if the fqdn has been queried before, and if it has then it references the cache for increased time efficiency
                        if ip in geolocation_cache.keys():
                            self._logger.debug("Geolocation cache for %s" % ip)
                            results.append(geolocation_cache[ip])
                            continue

                        #CIDR result fetching
                        cidr_trie_find_result = cidr_trie.find_all(ip)
                        if cidr_trie_find_result:
                            result_series = dbip_df.loc[cidr_trie_find_result[0][0]]
                            result_series = result_series.replace(np.nan, None)
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
