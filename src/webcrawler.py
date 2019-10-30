import argparse
from typing import List

from contentfetcher import ContentFetcher
from contentparsing import extract_urls


def setup_argument_parser():
    """
    Setup the argument parser for webcrawler
    :return: the argument parser
    """
    arg_parser = argparse.ArgumentParser(prog='src')
    # User needs to specify the URL from which to begin the search
    arg_parser.add_argument('url',
                            help='URL to start from')
    # User may provide a limit on how many URLs to see
    arg_parser.add_argument('-l', '--limit',
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
    A very simple web crawler
    """

    def __init__(self, user_agents: List[str]):
        self.content_fetcher = ContentFetcher(user_agents)

    def crawl(self, start_url, limit):
        """
        Crawl through
        :param start_url:
        :param limit:
        :return:
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
    web_crawler = WebCrawler(args.agents)
    found_urls = web_crawler.crawl(args.url, limit=args.limit)
    print(len(found_urls))
    for url in found_urls:
        print(url)
