import sys
sys.path.insert(0, r'../trackerhacker')
from unittest import mock
from unittest import TestCase
from browsermanager import WebBrowsers
import datacollection
import logging

logger = logging.getLogger('tracker_hacker')

class TestBrowsers(TestCase):
    # Test class for verifying that each browser can correctly collect data on each URL provided
    def test_chrome(self):
        urls = [
            'http://www.duckduckgo.com',
            'http://www.google.com',
            'http://www.cnn.com'
        ]
        for url in urls:
            result = datacollection.collect_request_urls(logger, [url], [WebBrowsers.CHROME])
            self.assertEqual(type(result), dict)
            self.assertTrue(url in result)
            self.assertEqual(type(result[url]), dict)
            self.assertTrue('WebBrowsers.CHROME' in result[url])
            self.assertTrue(len(result[url]['WebBrowsers.CHROME']) > 0)

    def test_firefox(self):
        urls = [
            'http://www.duckduckgo.com',
            'http://www.google.com',
            'http://www.cnn.com'
        ]
        for url in urls:
            result = datacollection.collect_request_urls(logger, [url], [WebBrowsers.FIREFOX])
            self.assertEqual(type(result), dict)
            self.assertTrue(url in result)
            self.assertEqual(type(result[url]), dict)
            self.assertTrue('WebBrowsers.FIREFOX' in result[url])
            self.assertTrue(len(result[url]['WebBrowsers.FIREFOX']) > 0)

    def test_edge(self):
        urls = [
            'http://www.duckduckgo.com',
            'http://www.google.com',
            'http://www.cnn.com'
        ]
        for url in urls:
            result = datacollection.collect_request_urls(logger, [url], [WebBrowsers.EDGE])
            self.assertEqual(type(result), dict)
            self.assertTrue(url in result)
            self.assertEqual(type(result[url]), dict)
            self.assertTrue('WebBrowsers.EDGE' in result[url])
            self.assertTrue(len(result[url]['WebBrowsers.EDGE']) > 0)
    
    def test_brave(self):
        urls = [
            'http://www.duckduckgo.com',
            'http://www.google.com',
            'http://www.cnn.com'
        ]
        for url in urls:
            result = datacollection.collect_request_urls(logger, [url], [WebBrowsers.BRAVE])
            self.assertEqual(type(result), dict)
            self.assertTrue(url in result)
            self.assertEqual(type(result[url]), dict)
            self.assertTrue('WebBrowsers.BRAVE' in result[url])
            self.assertTrue(len(result[url]['WebBrowsers.BRAVE']) > 0)