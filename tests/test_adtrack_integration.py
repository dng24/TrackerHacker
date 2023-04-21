import sys
sys.path.insert(0, r'../trackerhacker')
from unittest import mock
from unittest import TestCase
from browsermanager import WebBrowsers
import userinput
import datacollection
import adparsing
import logging

logger = logging.getLogger('tracker_hacker')

class TestAdtrackIntegration(TestCase):
    # Test class for verifying that the userinput and datacollection features work with each other
    @mock.patch('userinput.input', create=True)
    def test_default_list(self, mocked_input):
        url = 'http://www.google.com'
        mocked_input.side_effect = ['a', url, 'n']
        urls = userinput.urls()
        mocked_input.side_effect = 'b'
        browsers = userinput.browser_choice()
        mocked_input.side_effect = ['a', 'a']
        result = datacollection.collect_request_urls(logger, urls, browsers)
        self.assertEqual(type(result), dict)
        self.assertTrue(url in result)
        self.assertEqual(type(result[url]), dict)
        self.assertTrue('WebBrowsers.FIREFOX' in result[url])
        self.assertTrue(len(result[url]['WebBrowsers.FIREFOX']) > 0)