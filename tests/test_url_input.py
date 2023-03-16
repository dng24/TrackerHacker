import sys
import io
import os
import re
sys.path.insert(0, r'C:\Users\treba\Documents\GitHub\TrackerHacker\trackerhacker')
import userinput
from unittest import mock
from unittest import TestCase
from unittest import skip

class TestUIHelpQuitJunk(TestCase):
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('userinput.input', create=True)
    def test_datapoints_help(self, mocked_input, mock_stdout):
        possible_entry_helps = [
            ['h', 'q'],
            ['a', 'h', 'q'],
            ['a', 'y', 'b', 'h', 'q']
        ]
        for entry_help in possible_entry_helps:
            mocked_input.side_effect = entry_help
            result = userinput.datapoints()
            getvalue_result = mock_stdout.getvalue()
            self.assertTrue("Welcome to tracker hacker, a convenient tool" in getvalue_result)
            
if __name__ == "__main__":
    pass