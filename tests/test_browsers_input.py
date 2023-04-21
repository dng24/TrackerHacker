import sys
sys.path.insert(0, r'../trackerhacker')
import io
import os
import re
import userinput
from browsermanager import WebBrowsers
from unittest import mock
from unittest import TestCase
from unittest import skip

class TestBrowsersInput(TestCase):
    # Test class for verifying that the browser selection works properly
    @mock.patch('userinput.input', create=True)
    def test_browsers(self, mocked_input):
        # Test class for verifying that each choice functions correctly
        browser_inputs = [
            'a',
            'b',
            'c',
            'd'
        ]
        results_dict = {'a': WebBrowsers.CHROME, 'b': WebBrowsers.FIREFOX, 'c': WebBrowsers.EDGE, 'd': WebBrowsers.BRAVE}
        for browser_input in browser_inputs:
            mocked_input.side_effect = browser_input
            result = userinput.browser_choice()
            self.assertEqual(result, [results_dict[browser_input]])

    @mock.patch('userinput.input', create=True)
    def test_all_browsers(self, mocked_input):
        # Test class for verifying that the 'select all browsers' function works correctly
        mocked_input.side_effect = 'e'
        result = userinput.browser_choice()
        self.assertEqual(result, [WebBrowsers.CHROME, WebBrowsers.FIREFOX, WebBrowsers.EDGE, WebBrowsers.BRAVE])