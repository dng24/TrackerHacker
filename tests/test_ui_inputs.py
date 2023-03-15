import sys
import io
import os
import re
sys.path.insert(0, r'C:\Users\treba\Documents\GitHub\TrackerHacker\trackerhacker')
import userinput
from unittest import mock
from unittest import TestCase

class TestUIInputs(TestCase):
    @mock.patch('userinput.input', create=True)
    def test_datapoints_quit(self, mocked_input):
        possible_entry_quits = [
            ['q'],
            ['a', 'q'],
            ['a', 'y', 'b', 'q']
        ]
        for possible_entry_quit in possible_entry_quits:
            mocked_input.side_effect = possible_entry_quit
            result = userinput.datapoints()
            self.assertEqual(result, None)

    @mock.patch('userinput.input', create=True)
    def test_browser_choice_quit(self, mocked_input):
        possible_entry_quits = [
            ['q']
        ]
        for possible_entry_quit in possible_entry_quits:
            mocked_input.side_effect = possible_entry_quit
            result = userinput.browser_choice()
            self.assertEqual(result, None)

    @mock.patch('userinput.input', create=True)
    def test_urls_quit(self, mocked_input):
        possible_entry_quits = [
            ['q'],
            ['a', 'q'],
            ['a', 'http://www.duckduckgo.com', 'q'],
            ['a', 'http://www.duckduckgo.com', 'y', 'q']
        ]
        for possible_entry_quit in possible_entry_quits:
            mocked_input.side_effect = possible_entry_quit
            result = userinput.urls()
            print(possible_entry_quit)
            self.assertEqual(result, None)

    @mock.patch('userinput.input', create=True)
    def test_adtrack_list_quit(self, mocked_input):
        possible_entry_quits = [
            ['q'],
            ['b', 'q']
        ]
        for possible_entry_quit in possible_entry_quits:
            mocked_input.side_effect = possible_entry_quit
            result = userinput.adtrack_list()
            print(possible_entry_quit)
            self.assertEqual(result, None)

    @mock.patch('userinput.input', create=True)
    def test_datapoints_help(self, mocked_input):
        possible_entry_quits = [
            ['h', 'q'],
            ['a', 'h', 'q'],
            ['a', 'y', 'b', 'h', 'q']
        ]
        for possible_entry_quit in possible_entry_quits:
            mocked_input.side_effect = possible_entry_quit
            result = userinput.datapoints()
            self.assertEqual(result, None)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('userinput.input', create=True)
    def test_browser_choice_help(self, mocked_input, mock_stdout):
        possible_entry_quits = [
            ['h', 'q']
        ]
        for possible_entry_quit in possible_entry_quits:
            mocked_input.side_effect = possible_entry_quit
            result = userinput.browser_choice()
            getvalue_result = mock_stdout.getvalue()
            getvalue_result = repr(getvalue_result)
            #sys.stdout = sys.__stdout__
            self.assertRegex(getvalue_result, r".*Welcome to hacker tracker, a convenient tool.*")

    @mock.patch('userinput.input', create=True)
    def test_urls_help(self, mocked_input):
        possible_entry_quits = [
            ['h', 'q'],
            ['a', 'h', 'q'],
            ['a', 'http://www.duckduckgo.com', 'h', 'q'],
            ['a', 'http://www.duckduckgo.com', 'y', 'h', 'q']
        ]
        for possible_entry_quit in possible_entry_quits:
            mocked_input.side_effect = possible_entry_quit
            result = userinput.urls()
            print(possible_entry_quit)
            self.assertEqual(result, None)

    @mock.patch('userinput.input', create=True)
    def test_adtrack_list_help(self, mocked_input):
        possible_entry_quits = [
            ['h', 'q'],
            ['b', 'h', 'q']
        ]
        for possible_entry_quit in possible_entry_quits:
            mocked_input.side_effect = possible_entry_quit
            result = userinput.adtrack_list()
            print(possible_entry_quit)
            self.assertEqual(result, None)