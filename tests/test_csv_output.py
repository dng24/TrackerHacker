import sys
sys.path.insert(0, r'../trackerhacker')
from unittest import mock
from unittest import TestCase
from browsermanager import WebBrowsers
import datacollection
import logging

logger = logging.getLogger('tracker_hacker')

class TestCSVOutput(TestCase):
    def test_ddg_output(self):
        url = 'http://www.duckduckgo.com'
        result = datacollection.collect_request_urls(logger, [url], [WebBrowsers.FIREFOX])