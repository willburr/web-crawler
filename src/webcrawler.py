import argparse
from typing import List

from contentfetcher import ContentFetcher
from contentparsing import extract_urls


def setup_argument_parser():
    """
    Setup the argument parser for webcrawler.
    :return: the argument parser
    """
    arg_parser = argparse.ArgumentParser(prog='src')
    # User needs to specify the URL from which to begin the search
    arg_parser.add_argument('url',
                            help='URL to start from')
    # User may provide a limit on how many URLs to see
    arg_parser.add_argument('-l', '--limit',
                            dest='limit',
                            type=int,
                            help='number of URLs to display, 100 by default',
                            default=100)
    # User may provide a list of user agents to cycle through
    arg_parser.add_argument('-ua' '--user-agents',
                            dest='agents',
                            nargs='*',
                            help='user agent(s) to use for requests',
                            default=[])
    return arg_parser


class WebCrawler:
    """
    A very simple web crawler.
    """

    def __init__(self, content_fetcher: ContentFetcher):
        self.content_fetcher = content_fetcher

    def discover(self, start_url: str, limit: int) -> List[str]:
        """
        Fetch the url provided and retrieve links, subsequently fetching
        the pages at those links until reaching limit (or running out of links).
        :param start_url: url to start from
        :param limit: number of urls to return in list
        :return: list of urls discovered
        """
        urls = [start_url]
        seen = {start_url: True}
        count = 1
        while len(urls) > 0 and count < limit:
            url = urls.pop()
            contents = self.content_fetcher.retrieve_page(url)
            new_urls = filter(lambda x: x not in seen, extract_urls(url, contents))
            for new_url in new_urls:
                if count == limit:
                    break
                urls.append(new_url)
                seen[new_url] = True
                count += 1
        return list(seen.keys())


if __name__ == "__main__":
    parser = setup_argument_parser()
    args = parser.parse_args()
    web_crawler = WebCrawler(ContentFetcher(args.agents))
    found_urls = web_crawler.discover(args.url, limit=args.limit)
    for url in found_urls:
        print(url)
