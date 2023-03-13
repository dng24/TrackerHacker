import sys
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
    def test_datapoints_quit(self, mocked_input):
        possible_entry_quits = [
            ['h'],
            ['a', 'h'],
            ['a', 'y', 'b', 'h']
        ]
        for possible_entry_quit in possible_entry_quits:
            mocked_input.side_effect = possible_entry_quit
            result = userinput.datapoints()
            self.assertEqual(result, None)

    @mock.patch('userinput.input', create=True)
    def test_browser_choice_quit(self, mocked_input):
        possible_entry_quits = [
            ['h']
        ]
        for possible_entry_quit in possible_entry_quits:
            mocked_input.side_effect = possible_entry_quit
            result = userinput.browser_choice()
            self.assertEqual(result, None)

    @mock.patch('userinput.input', create=True)
    def test_urls_quit(self, mocked_input):
        possible_entry_quits = [
            ['h'],
            ['a', 'h'],
            ['a', 'http://www.duckduckgo.com', 'h'],
            ['a', 'http://www.duckduckgo.com', 'y', 'h']
        ]
        for possible_entry_quit in possible_entry_quits:
            mocked_input.side_effect = possible_entry_quit
            result = userinput.urls()
            print(possible_entry_quit)
            self.assertEqual(result, None)

    @mock.patch('userinput.input', create=True)
    def test_adtrack_list_quit(self, mocked_input):
        possible_entry_quits = [
            ['h'],
            ['b', 'h']
        ]
        for possible_entry_quit in possible_entry_quits:
            mocked_input.side_effect = possible_entry_quit
            result = userinput.adtrack_list()
            print(possible_entry_quit)
            self.assertEqual(result, None)