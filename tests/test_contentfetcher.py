import unittest
import gzip
import zlib

from contentfetcher import ContentFetcher


class TestContentFetcher(unittest.TestCase):
    user_agents = ["Mozilla", "Python", "Something Else"]
    url = "https://crawler-test.com/"

    def setUp(self) -> None:
        self.content_fetcher = ContentFetcher(self.user_agents)

    def test_get_next_user_agent_cycles_through_agents(self):
        self.assertEqual(self.content_fetcher.get_next_user_agent(), "Mozilla")
        self.assertEqual(self.content_fetcher.get_next_user_agent(), "Python")
        self.assertEqual(self.content_fetcher.get_next_user_agent(), "Something Else")
        self.assertEqual(self.content_fetcher.get_next_user_agent(), "Mozilla")

    def test_get_next_user_agent_cycles_returns_none_when_none_given(self):
        content_fetcher_no_agents = ContentFetcher([])
        self.assertIsNone(content_fetcher_no_agents.get_next_user_agent())

    def test_construct_request_adds_correct_headers(self):
        request = self.content_fetcher.construct_request(self.url)
        self.assertEqual(request.get_header("User-agent"), "Mozilla")
        self.assertEqual(request.get_header("Accept-encoding"), "gzip, deflate")
        self.assertEqual(request.get_full_url(), self.url)
        self.assertEqual(request.get_header("Accept"), "text/html")

    def test_decompress_content_handles_gzip(self):
        test_bytes = "Compress me".encode('utf-8')
        compressed_data = gzip.compress(test_bytes)
        self.assertEqual(self.content_fetcher.decompress_content(compressed_data, "gzip"), test_bytes)

    def test_decompress_content_handles_deflate(self):
        test_bytes = "Compress me".encode('utf-8')
        compressed_data = zlib.compress(test_bytes)
        self.assertEqual(self.content_fetcher.decompress_content(compressed_data, "deflate"), test_bytes)

    def test_decompress_content_recovers_when_unknown_format(self):
        test_bytes = "Compress me".encode('utf-8')
        compressed_data = zlib.compress(test_bytes)
        self.assertEqual(self.content_fetcher.decompress_content(compressed_data, "unknown"), ''.encode('utf-8'))

    def test_handle_response_can_handle_gzip_content(self):
        test_string = "Compress me"
        compressed_data = gzip.compress(test_string.encode('utf-8'))
        headers = [("Content-Encoding", "gzip")]
        self.assertEqual(self.content_fetcher.handle_response(headers, compressed_data), test_string)

    def test_handle_response_can_handle_deflate_content(self):
        test_string = "Compress me"
        compressed_data = zlib.compress(test_string.encode('utf-8'))
        headers = [("Content-Encoding", "deflate")]
        self.assertEqual(self.content_fetcher.handle_response(headers, compressed_data), test_string)
