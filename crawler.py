from urllib import request
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from html.parser import HTMLParser


class LinkTagParser(HTMLParser):

    def __init__(self, scheme, hostname, seen):
        super().__init__()
        self.new_urls = []
        self.scheme = scheme
        self.hostname = hostname
        self.seen = seen

    def parse_link(self, link):
        parse_result = urlparse(link)
        new_link = parse_result.geturl()
        if not parse_result.hostname:
            new_link = self.hostname + parse_result.path
        self.new_urls.append(new_link)

    def handle_starttag(self, tag, attrs):
        # Only interested in <a> tags
        if tag != 'a':
            return
        for attr in attrs:
            if attr[0] == 'href':
                self.parse_link(attr[1])


    def error(self, message):
        """
        Handle error
        :param message:
        """
        print(message)

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
            parsed_url = urlparse(url)
            parser = LinkTagParser(parsed_url.scheme, parsed_url.hostname, seen)
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
