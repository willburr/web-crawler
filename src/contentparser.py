import html.parser
from typing import List
from urlhandling import *


class ContentParser:

    def parse(self, url: str, content: str) -> List[str]:
        html_parser = HTMLLinkParser()
        html_parser.feed(content)
        absolute_urls, other_urls = [], []
        for new_url in html_parser.new_urls:
            (absolute_urls if is_http_url(new_url) else other_urls).append(new_url)
        relative_urls = filter(lambda u: is_relative_url(u), other_urls)
        combined_urls = list(map(lambda u: construct_absolute_url(url, u), relative_urls))
        return list(map(normalise_url, absolute_urls + combined_urls))


class HTMLLinkParser(html.parser.HTMLParser):

    def __init__(self):
        super().__init__()
        self.new_urls = []

    def handle_starttag(self, tag, attrs):
        # Only interested in <a> tags
        if tag != 'a':
            return
        for attr in attrs:
            if attr[0] == 'href':
                self.new_urls.append(attr[1])

    def error(self, message):
        """
        Handle error
        :param message:
        """
        print(message)
