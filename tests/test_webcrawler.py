import unittest
import unittest.mock

from webcrawler import WebCrawler


class TestWebCrawler(unittest.TestCase):

    def setUp(self) -> None:
        self.content_fetcher = unittest.mock.Mock()
        self.content_fetcher.retrieve_page.return_value = self.generate_mock_page()
        self.web_crawler = WebCrawler(self.content_fetcher)

    def generate_mock_page(self):
        return "<!DOCTYPE html>" \
               "<html><body><h1>Some header</h1><p>Some text</p>" \
               "<a href='http://some_link2.com'></a>" \
               "<a href='http://some_link2.com'></a>" \
               "</body></html>"

    def test_crawl_does_not_return_duplicate_links(self):
        urls = self.web_crawler.crawl("http://some_link.com", limit=10)
        self.assertEqual(urls, ["http://some_link.com", "http://some_link2.com"])

    def test_crawl_does_not_give_more_links_than_the_limit(self):
        urls = self.web_crawler.crawl("http://some_link.com", limit=1)
        self.assertEqual(urls, ["http://some_link.com"])
