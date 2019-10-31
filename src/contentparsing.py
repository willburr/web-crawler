import html.parser
from typing import List

from urlhandling import *


def extract_urls(origin_url: str, content: str) -> List[str]:
    """
    Extract the urls from within the content that was retrieved from origin url.
    :param origin_url: url from which the content was fetched from
    :param content: content to parse
    :return: list of unique urls identified within the content
    """
    html_parser = HTMLLinkParser(origin_url=origin_url)
    html_parser.feed(content)
    return list(map(normalise_url, html_parser.new_urls))


class HTMLLinkParser(html.parser.HTMLParser):
    """
    HTML Parser that specifically extracts links from
    <a> tags.
    If there is a relative link, then it uses the origin url to
    construct the absolute link.
    """

    def __init__(self, origin_url: str):
        """
        :param origin_url: URL from which the content has been fetched from
        """
        super().__init__()
        self.new_urls = []
        self.origin_url = origin_url

    def process_link(self, link: str):
        """
        Converts link to an absolute (HTTP) URL if possible.
        :param link: link identified within tag
        """
        if is_http_url(link):
            self.new_urls.append(link)
        if is_relative_url(link):
            self.new_urls.append(construct_absolute_url(self.origin_url, link))

    def handle_starttag(self, tag, attrs):
        """
        :param tag: the HTML tag
        :param attrs: attributes in the tag
        """
        # Only interested in <a> tags
        if tag != 'a':
            return
        for attr in attrs:
            if attr[0] == 'href':
                self.process_link(attr[1])
                break

    def error(self, message):
        """
        Handle error, required when extending HTMLParser
        :param message:
        """
        print(message)
