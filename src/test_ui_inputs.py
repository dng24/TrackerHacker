from unittest import mock
from unittest import TestCase
from browsers import WebBrowsers
import userinput

class TestUIInputs(TestCase):
    @mock.patch('userinput.input', create=True)
    def test_immediate_quit(self, mocked_input):
        mocked_input.side_effect = ['q']
        result = userinput.get_user_input()
        self.assertEqual(result, 0)

    @mock.patch('userinput.input', create=True)
    def test_whois_firefox_manual_ddg_default(self, mocked_input):
        mocked_input.side_effect = ['a', 'no', 'b', 'a', 'http://www.duckduckgo.com', 'no', 'a']
        result = userinput.get_user_input()
        self.assertTupleEqual(result, (['a'], WebBrowsers.FIREFOX, ['http://www.duckduckgo.com'], []))