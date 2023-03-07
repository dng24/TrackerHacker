from unittest import mock
from unittest import TestCase
from trackerhacker.browsermanager import WebBrowsers
from trackerhacker import userinput

class TestUIInputs(TestCase):
    @mock.patch('userinput.input', create=True)
    def test_datapoints_quit(self, mocked_input):
        mocked_input.side_effect = ['q']
        result = userinput.datapoints()
        self.assertEqual(result, None)

    @mock.patch('userinput.input', create=True)
    def test_datapoints_a(self, mocked_input):
        mocked_input.side_effect = ['a', 'n']
        result = userinput.datapoints()
        self.assertListEqual(result, ['a'])

    @mock.patch('userinput.input', create=True)
    def test_url_immediate_quit(self, mocked_input):
        mocked_input.side_effect = ['q']
        result = userinput.urls()
        self.assertEqual(result, None)

    @mock.patch('userinput.input', create=True)
    def test_url_manual_quit(self, mocked_input):
        mocked_input.side_effect = ['a', 'q']
        result = userinput.urls()
        self.assertEqual(result, None)