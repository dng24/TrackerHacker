import sys
sys.path.insert(0, r'../trackerhacker')
import io
import os
import re
import userinput
from unittest import mock
from unittest import TestCase
from unittest import skip

class TestDatapointsInput(TestCase):
    @mock.patch('userinput.input', create=True)
    def test_datapoints(self, mocked_input):
        browser_inputs = [
            ['a', 'n'],
            ['a', 'y', 'b', 'n']
        ]
        i = 0
        results = [['a'], ['a', 'b']]
        for browser_input in browser_inputs:
            mocked_input.side_effect = browser_input
            result = userinput.datapoints()
            self.assertEqual(result, results[i])
            i += 1