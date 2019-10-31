from urlhandling import *
import unittest


class TestURLHandling(unittest.TestCase):
    valid_http_urls = ["http://localhost/", "https://www.google.com"]
    invalid_http_urls = ["mailto:me", "just not a url", "www.google.com", "http://"]

    valid_relative_urls = ["/index.html", "robots.txt", "/"]

    def test_is_http_url_correctly_identifies_valid_http_urls(self):
        for http_url in self.valid_http_urls:
            self.assertTrue(is_http_url(http_url))

    def test_is_http_url_correctly_identifies_invalid_http_urls(self):
        for invalid_url in self.invalid_http_urls:
            self.assertFalse(is_http_url(invalid_url))

    def test_is_relative_url_correctly_identifies_valid_relative_urls(self):
        for relative_url in self.valid_relative_urls:
            self.assertTrue(is_relative_url(relative_url))

    def test_is_relative_url_correctly_identifies_non_relative_urls(self):
        for absolute_url in self.valid_http_urls:
            self.assertFalse(is_relative_url(absolute_url))

    def test_construct_absolute_url_correctly_combines_url_and_path(self):
        absolute_url_1 = construct_absolute_url(self.valid_http_urls[0], self.valid_relative_urls[0])
        self.assertEqual(absolute_url_1, "http://localhost/index.html")
        absolute_url_2 = construct_absolute_url(self.valid_http_urls[0], self.valid_relative_urls[1])
        self.assertEqual(absolute_url_2, "http://localhost/robots.txt")
