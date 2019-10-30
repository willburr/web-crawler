import html.parser
from typing import List


class LinkContentParser:

    def parse(self, content: str) -> List[str]:
        html_parser = HTMLLinkParser()
        html_parser.feed(content)
        return html_parser.new_urls


class HTMLLinkParser(html.parser.HTMLParser):

    def __init__(self):
        super().__init__()
        self.new_urls = []

    def handle_starttag(self, tag, attrs):
        # Only interested in <a> tags
        if tag != 'a':
            return
        for attr in attrs:
            if attr[0] == 'href' and attr[1].startswith("http"):
                self.new_urls.append(attr[1])

    def error(self, message):
        """
        Handle error
        :param message:
        """
        print(message)
