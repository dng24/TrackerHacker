import sys
sys.path.insert(0, r'../trackerhacker')
import datacollection
import analysis
import io
import os
import re
import logging
import json
from browsermanager import WebBrowsers
from unittest import mock
from unittest import TestCase
from unittest import skip

logger = logging.getLogger('tracker_hacker')

class TestAnalysis(TestCase):
    # Test class for the analysis section of parsed ads/trackers
    def test_init(self):
        # Tests that the Analysis class can actually load and read in the data
        test_data = self._read_test_data('ddg_test_data.txt')
        analysis_test = analysis.Analysis(logger, test_data)
        self.assertTrue(analysis_test.results)
        self.assertTrue('http://www.duckduckgo.com' in analysis_test.results)
        self.assertTrue('Firefox' in analysis_test.results['http://www.duckduckgo.com'])

    def test_whois(self):
        # Tests that the whois functionality works and outputs a whois result in the results dict
        test_data = self._read_test_data('ddg_test_data.txt')
        analysis_test = analysis.Analysis(logger, test_data)
        results = analysis_test.results
        analysis_test.do_whois_analysis()
        whois = results['http://www.duckduckgo.com']['Firefox']['www.duckduckgo.com']["whois"]
        self.assertTrue('whois_server' in whois)
        self.assertTrue(whois['whois_server'])

    def test_server_location(self):
        # Tests that the server location analysis functionality works properly and outputs a result in the dict
        test_data = self._read_test_data('ddg_test_data.txt')
        analysis_test = analysis.Analysis(logger, test_data)
        results = analysis_test.results
        analysis_test.do_server_location_analysis()
        server_location = results['http://www.duckduckgo.com']['Firefox']['www.duckduckgo.com']["server_location"]
        self.assertTrue(type(server_location[0]) == dict)

    def _get_test_data(url, fname):
        result = datacollection.collect_request_urls(logger, [url], [WebBrowsers.FIREFOX])
        with open(f'test_data/{fname}', 'w') as f:
            json.dump(result, f)
            f.close()

    def _read_test_data(self, fname):
        with open(f'test_data/{fname}', 'r') as f:
            test_data = json.load(f)
        return test_data

if __name__ == "__main__":
    TestAnalysis._get_test_data('http://www.cnn.com', 'cnn_test_data.txt')
        