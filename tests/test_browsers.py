from unittest import mock
from unittest import TestCase
from browsermanager import WebBrowsers
import datacollection

class TestBrowsers(TestCase):
    def test_chrome(self):
        result = datacollection.collect_fqdns(['http://www.duckduckgo.com'], [WebBrowsers.CHROME])
        self.assertEqual(result, 0)

    def test_firefox(self):
        result = datacollection.collect_fqdns(['http://www.duckduckgo.com'], [WebBrowsers.FIREFOX])
        self.assertEqual(result, 0)

    def test_edge(self):
        result = datacollection.collect_fqdns(['http://www.duckduckgo.com'], [WebBrowsers.EDGE])
        self.assertEqual(result, 0)
    
    def test_brave(self):
        result = datacollection.collect_fqdns(['http://www.duckduckgo.com'], [WebBrowsers.BRAVE])
        self.assertEqual(result, 0)