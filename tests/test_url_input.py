import sys
sys.path.insert(0, r'../trackerhacker')
import userinput
import io
import os
import re
from unittest import mock
from unittest import TestCase
from unittest import skip

class TestURLInput(TestCase):
    # Test class for ensuring that various types of URL entries are handled correctly
    @mock.patch('userinput.input', create=True)
    def test_manual_entry_success(self, mocked_input):
        # Test to ensure manually entered valid urls are stored
        mocked_input.side_effect = ['a', 'http://www.duckduckgo.com', 'n']
        result = userinput.urls()
        self.assertEquals(result, ['http://www.duckduckgo.com'])

    @mock.patch('userinput.input', create=True)
    def test_manual_correctly_formatted_unreachable(self, mocked_input):
        # Tests that an unreachable, but correctly formatted, URL is stored properly
        mocked_input.side_effect = ['a', 'http://www.fghydsuiagbiucygsduagsdiucyagshjzgxchkvdsadfahkj.com', 'n']
        result = userinput.urls()
        self.assertEquals(result, ['http://www.fghydsuiagbiucygsduagsdiucyagshjzgxchkvdsadfahkj.com'])

    @mock.patch('userinput.input', create=True)
    def test_manual_junk(self, mocked_input):
        # Tests that junk inputs are discarded
        junk_inputs = [
            ['a', 'htp:/www.duckduckgo.com', 'q'],
            ['a', 'fjdsk', 'q'],
            ['a', '', 'q'],
            ['a', '113', 'q'],
            ['a', '%', 'q'],
            ['a', '\n', 'q'],
        ]
        for junk_input in junk_inputs:
            sys.stdout = io.StringIO()
            mocked_input.side_effect = junk_input
            userinput.urls()
            self.assertTrue('Malformed URL entered', sys.stdout.getvalue())
            sys.stdout = sys.__stdout__
    
    @mock.patch('userinput.input', create=True)
    def test_file_exists(self, mocked_input):
        # Tests that files passed in with varying amounts of valid/malformed URLs are all handled properly
        fp_inputs = [
            (['b', 'url_files/test1.txt'], []),
            (['b', 'url_files/test2.txt'], ['http://www.duckduckgo.com']),
            (['b', 'url_files/test3.txt'], ['http://www.fsdgyauifgauiys.com']),
            (['b', 'url_files/test4.txt'], False),
            (['b', 'url_files/test5.txt'], False),
            (['b', 'url_files/test5.txt'], ['http://www.duckduckgo.com'])
        ]
        for fp in fp_inputs:
            sys.stdout = io.StringIO()
            mocked_input.side_effect = fp[0]
            result = userinput.urls()
            if type(fp[1]) == list:
                self.assertListEqual(result, fp[1])
            else:
                self.assertTrue("Malformed urls included in your file." in sys.stdout.getvalue(), f"Failed on {fp}, getvalue: {sys.stdout.getvalue()}")
            sys.stdout = sys.__stdout__

    @mock.patch('userinput.input', create=True)
    def test_file_not_exists(self, mocked_input):
        # Tests that if the file doesn't exists, it outputs the correct message to the user
        fp_inputs = [
            ['b', 'url_files/test6.txt', 'q'],
            ['b', 'asdf', 'q'],
            ['b', '123', 'q'],
            ['b', '%', 'q'],
            ['b', '\n', 'q'],
            ['b', '', 'q']
        ]
        for fp in fp_inputs:
            sys.stdout = io.StringIO()
            mocked_input.side_effect = fp
            result = userinput.urls()
            self.assertTrue("Oops! Looks like there was a problem referencing the file." in sys.stdout.getvalue(), f"Failed on {fp}, getvalue: {sys.stdout.getvalue()}")
            sys.stdout = sys.__stdout__

if __name__ == "__main__":
    pass