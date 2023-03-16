import sys
sys.path.insert(0, r'../trackerhacker')
from unittest import mock
from unittest import TestCase
from browsermanager import WebBrowsers
import userinput
import datacollection
import logging

logger = logging.getLogger('tracker_hacker')

class TestUIBrowserIntegration(TestCase):
    @mock.patch('userinput.input', create=True)
    def test_chrome_ui(self, mocked_input):
        url = 'http://www.duckduckgo.com'
        mocked_input.side_effect = ['a', url, 'n']
        urls = userinput.urls()
        mocked_input.side_effect = 'a'
        browsers = userinput.browser_choice()
        result = datacollection.collect_request_urls(logger, urls, browsers)
        self.assertEqual(type(result), dict)
        self.assertTrue(url in result)
        self.assertEqual(type(result[url]), dict)
        self.assertTrue('WebBrowsers.CHROME' in result[url])
        self.assertTrue(len(result[url]['WebBrowsers.CHROME']) > 0)

    @mock.patch('userinput.input', create=True)
    def test_firefox_ui(self, mocked_input):
        url = 'http://www.duckduckgo.com'
        mocked_input.side_effect = ['a', url, 'n']
        urls = userinput.urls()
        mocked_input.side_effect = 'b'
        browsers = userinput.browser_choice()
        result = datacollection.collect_request_urls(logger, urls, browsers)
        self.assertEqual(type(result), dict)
        self.assertTrue(url in result)
        self.assertEqual(type(result[url]), dict)
        self.assertTrue('WebBrowsers.FIREFOX' in result[url])
        self.assertTrue(len(result[url]['WebBrowsers.FIREFOX']) > 0)

    @mock.patch('userinput.input', create=True)
    def test_edge_ui(self, mocked_input):
        url = 'http://www.duckduckgo.com'
        mocked_input.side_effect = ['a', url, 'n']
        urls = userinput.urls()
        mocked_input.side_effect = 'c'
        browsers = userinput.browser_choice()
        result = datacollection.collect_request_urls(logger, urls, browsers)
        self.assertEqual(type(result), dict)
        self.assertTrue(url in result)
        self.assertEqual(type(result[url]), dict)
        self.assertTrue('WebBrowsers.EDGE' in result[url])
        self.assertTrue(len(result[url]['WebBrowsers.EDGE']) > 0)
    
    @mock.patch('userinput.input', create=True)
    def test_brave_ui(self, mocked_input):
        url = 'http://www.duckduckgo.com'
        mocked_input.side_effect = ['a', url, 'n']
        urls = userinput.urls()
        mocked_input.side_effect = 'd'
        browsers = userinput.browser_choice()
        result = datacollection.collect_request_urls(logger, urls, browsers)
        self.assertEqual(type(result), dict)
        self.assertTrue(url in result)
        self.assertEqual(type(result[url]), dict)
        self.assertTrue('WebBrowsers.BRAVE' in result[url])
        self.assertTrue(len(result[url]['WebBrowsers.BRAVE']) > 0)