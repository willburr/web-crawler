from urllib import request
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse

from linkparsers.externallinkparser import ExternalLinkParser


class WebCrawler:
    """
    A very simple web crawler
    """

    def retrieve_page(self, url):
        url_request = request.Request(url)
        try:
            return request.urlopen(url_request).read().decode("utf-8")
        except HTTPError:
            return ""
        except URLError:
            return ""

    def crawl(self, start_url, limit):
        urls = [start_url]
        seen = {start_url: True}
        count = 0
        while len(urls) > 0 and count < limit:
            url = urls.pop()
            contents = self.retrieve_page(url)
            parser = ExternalLinkParser(seen)
            parser.feed(contents)
            new_urls = parser.new_urls
            index = 0
            while index < len(new_urls) and count < limit:
                new_url = new_urls[index]
                urls.append(new_url)
                seen[new_url] = True
                count += 1
                index += 1
        return list(seen.keys())


if __name__ == "__main__":
    web_crawler = WebCrawler()
    urls = web_crawler.crawl("", limit=50)
    print(urls)
