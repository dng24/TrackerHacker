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

class TestAdtrackListInput(TestCase):
    @mock.patch('userinput.input', create=True)
    def test_default_list(self, mocked_input):
        mocked_input.side_effect = ['a', 'a']
        result = userinput.adtrack_list()
        self.assertTupleEqual(result, (True, ""))

    @mock.patch('userinput.input', create=True)
    def test_file_exists(self, mocked_input):
        mocked_input.side_effect = ['n', 'adtrack_list_files/test1.txt']
        result = userinput.adtrack_list()
        self.assertTupleEqual(result, (False, "adtrack_list_files/test1.txt"))

    #NOTE: does not work as intended
    @skip("not working correctly")
    @mock.patch('userinput.input', create=True)
    def test_file_invalid(self, mocked_input):
        sys.stdout = io.StringIO()
        mocked_input.side_effect = ['n', '%\n', 'q']
        result = userinput.adtrack_list()
        getvalue_result = sys.stdout.getvalue()
        self.assertTupleEqual(result, (None, None))
        self.assertTrue('error in processing filepath' in getvalue_result)