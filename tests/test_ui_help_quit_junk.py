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
            self.assertTupleEqual(result, (None, None))

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
            self.assertTrue("Welcome to tracker hacker, a convenient tool" in getvalue_result)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('userinput.input', create=True)
    def test_urls_help(self, mocked_input, mock_stdout):
        possible_entry_helps = [
            ['h', 'q'],
            ['a', 'h', 'q'],
            ['a', 'http://www.duckduckgo.com', 'h', 'q'],
            ['a', 'http://www.duckduckgo.com', 'y', 'h', 'q']
        ]
        for entry_help in possible_entry_helps:
            mocked_input.side_effect = entry_help
            result = userinput.urls()
            getvalue_result = mock_stdout.getvalue()
            self.assertTrue("Welcome to tracker hacker, a convenient tool" in getvalue_result)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('userinput.input', create=True)
    def test_adtrack_list_help(self, mocked_input, mock_stdout):
        possible_entry_helps = [
            ['h', 'q'],
            ['b', 'h', 'q']
        ]
        for entry_help in possible_entry_helps:
            mocked_input.side_effect = entry_help
            result = userinput.adtrack_list()
            getvalue_result = mock_stdout.getvalue()
            self.assertTrue("Welcome to tracker hacker, a convenient tool" in getvalue_result)

    #@skip("temp")
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('userinput.input', create=True)
    def test_datapoints_junk(self, mocked_input, mock_stdout):
        #TODO test for all possible entry points
        possible_junk_inputs = [
            ['u', 'q'],
            ['1', 'q'],
            ['%', 'q'],
            ['', 'q'],
            ['\n', 'q']
        ]
        for junk_input in possible_junk_inputs:
            mocked_input.side_effect = junk_input
            result = userinput.datapoints()
            getvalue_result = mock_stdout.getvalue()
            try:
                self.assertTrue("Something went wrong" in getvalue_result, \
                                f'Failed on junk input {junk_input}, getvalue_result: {getvalue_result}')
            except AssertionError as ae:
                print(f"Failed on junk input {junk_input}")
                print(str(ae))
                raise

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('userinput.input', create=True)
    def test_browser_choice_junk(self, mocked_input, mock_stdout):
        #TODO test for all possible entry points
        possible_junk_inputs = [
            ['u', 'q'],
            ['1', 'q'],
            ['%', 'q'],
            ['', 'q'],
            ['\n', 'q']
        ]
        for junk_input in possible_junk_inputs:
            mocked_input.side_effect = junk_input
            result = userinput.browser_choice()
            getvalue_result = mock_stdout.getvalue()
            try:
                self.assertTrue("Please enter a valid choice for browser" in getvalue_result, \
                                f'Failed on junk input {junk_input}, getvalue_result: {getvalue_result}')
            except AssertionError as ae:
                print(f"Failed on junk input {junk_input}")
                print(str(ae))
                raise

    
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('userinput.input', create=True)
    def test_urls_junk(self, mocked_input, mock_stdout):
        #TODO test for all possible entry points
        possible_junk_inputs = [
            ['u', 'q'],
            ['1', 'q'],
            ['%', 'q'],
            ['', 'q'],
            ['\n', 'q']
        ]
        for junk_input in possible_junk_inputs:
            mocked_input.side_effect = junk_input
            result = userinput.urls()
            getvalue_result = mock_stdout.getvalue()
            try:
                self.assertTrue("Please enter a valid input" in getvalue_result, \
                                f'Failed on junk input {junk_input}, getvalue_result: {getvalue_result}')
            except AssertionError as ae:
                print(f"Failed on junk input {junk_input}")
                print(str(ae))
                raise
            
    @skip("Not valid, probably")
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('userinput.input', create=True)
    def test_adtrack_list_junk(self, mocked_input, mock_stdout):
        #TODO test for all possible entry points
        possible_junk_inputs = [
            ['u', 'q'],
            ['1', 'q'],
            ['%', 'q'],
            ['', 'q'],
            ['\n', 'q']
        ]
        for junk_input in possible_junk_inputs:
            mocked_input.side_effect = junk_input
            result = userinput.adtrack_list()
            getvalue_result = mock_stdout.getvalue()
            try:
                self.assertTrue("Please enter a valid input" in getvalue_result, \
                                f'Failed on junk input {junk_input}, getvalue_result: {getvalue_result}')
            except AssertionError as ae:
                print(f"Failed on junk input {junk_input}")
                print(str(ae))
                raise

if __name__ == "__main__":
    pass