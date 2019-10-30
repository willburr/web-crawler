import html.parser
from typing import List
from urlhandling import *


class ContentParser:

    def parse(self, url: str, content: str) -> List[str]:
        html_parser = HTMLLinkParser(origin_url=url)
        html_parser.feed(content)
        return list(map(normalise_url, html_parser.new_urls))


class HTMLLinkParser(html.parser.HTMLParser):

    def __init__(self, origin_url):
        super().__init__()
        self.new_urls = []
        self.origin_url = origin_url

    def process_link(self, link):
        if is_http_url(link):
            self.new_urls.append(link)
        if is_relative_url(link):
            self.new_urls.append(construct_absolute_url(self.origin_url, link))


    def handle_starttag(self, tag, attrs):
        # Only interested in <a> tags
        if tag != 'a':
            return
        for attr in attrs:
            if attr[0] == 'href':
                self.process_link(attr[1])
                break

    def error(self, message):
        """
        Handle error
        :param message:
        """
        print(message)
