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
    @mock.patch('userinput.input', create=True)
    def test_browsers(self, mocked_input):
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