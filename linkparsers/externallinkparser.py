import html.parser


class ExternalLinkParser(html.parser.HTMLParser):

    def __init__(self, seen):
        super().__init__()
        self.new_urls = []
        self.seen = seen

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
