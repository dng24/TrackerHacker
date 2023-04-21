import sys
sys.path.insert(0, r'../trackerhacker')
import io
import os
import re
import logging
import json
import adparsing
from browsermanager import WebBrowsers
from unittest import TestCase
from unittest import skip

logger = logging.getLogger('tracker_hacker')

class TestAdparsing(TestCase):
    # Test class for the adparsing functionality of trackerhacker
    def test_extract_ads_trackers_ddg(self):
        # Grabs test data and checks that 'impression', the only tracker present on duckduckgo.com, is in the parsed URLS
        ddg_request_urls = self._read_test_data('ddg_test_data.txt')
        parsed_request_urls = adparsing.extract_ads_and_trackers(logger, '../adlists', ddg_request_urls)
        improving_urls = parsed_request_urls['http://www.duckduckgo.com']['Firefox']['improving.duckduckgo.com']
        impression_check = False
        for url_str in improving_urls:
            if 'impression' in url_str:
                impression_check = True
                break
        self.assertTrue(impression_check)

    def _read_test_data(self, fname):
        with open(f'test_data/{fname}', 'r') as f:
            test_data = json.load(f)
        return test_data

if __name__ == "__main__":
    tap = TestAdparsing(None)