import unittest

from contentparsing import extract_urls


class TestContentParsing(unittest.TestCase):

    origin_url = "https://crawler-test.com/"
    html_no_link = "<!DOCTYPE html><html><body><h1>Some header</h1><p>Some text</p></body></html>"
    html_link_in_text = "<!DOCTYPE html><html><body><h1>https://crawler-test.com/</h1><p>Some text</p></body></html>"
    html_relative_link_in_tag = "<!DOCTYPE html><html><body><h1>Some header/</h1><p>Some text</p>" \
                       "<a href='/hello.txt'></a>" \
                       "</body></html>"
    html_absolute_link_in_tag = "<!DOCTYPE html><html><body><h1>Some header</h1><p>Some text</p>" \
                                "<a href='https://crawler-test.com'></a>" \
                                "</body></html>"

    def test_extract_links_finds_no_links_when_not_present(self):
        self.assertEqual(extract_urls(self.origin_url, self.html_no_link), [])

    def test_extract_links_does_not_find_link_outside_atags(self):
        self.assertEqual(extract_urls(self.origin_url, self.html_link_in_text), [])

    def test_extract_links_resolves_relative_link_in_atag(self):
        self.assertEqual(extract_urls(self.origin_url, self.html_relative_link_in_tag),
                         ["https://crawler-test.com/hello.txt"])

    def test_extract_links_finds_absolute_link_in_atag(self):
        self.assertEqual(extract_urls(self.origin_url, self.html_absolute_link_in_tag),
                         ["https://crawler-test.com"])

