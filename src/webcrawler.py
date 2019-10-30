import argparse
from typing import List

from contentfetcher import ContentFetcher
from contentparser import ContentParser

parser = argparse.ArgumentParser(prog='src')
parser.add_argument('url',
                    help='URL to start from')
parser.add_argument('-l', '--limit',
                    type=int,
                    help='number of URLs to display',
                    default=50)
parser.add_argument('-d', '--delay',
                    type=float,
                    help='delay in seconds between each request',
                    default=0)
parser.add_argument('-ua' '--user-agents',
                    dest='agents',
                    nargs='*',
                    help='user agent(s) to use for requests',
                    default=[])


class WebCrawler:
    """
    A very simple web crawler
    """

    def __init__(self, user_agents: List[str]):
        self.content_parser = ContentParser()
        self.content_fetcher = ContentFetcher(user_agents)

    def crawl(self, start_url, limit):
        urls = [start_url]
        seen = {start_url: True}
        count = 0
        while len(urls) > 0 and count < limit:
            url = urls.pop()
            contents = self.content_fetcher.retrieve_page(url)
            new_urls = self.content_parser.parse(contents)
            index = 0
            while index < len(new_urls) and count < limit:
                new_url = new_urls[index]
                urls.append(new_url)
                seen[new_url] = True
                count += 1
                index += 1
        return list(seen.keys())


if __name__ == "__main__":
    args = parser.parse_args()
    web_crawler = WebCrawler(args.agents)
    found_urls = web_crawler.crawl(args.url, limit=args.limit)
    print(found_urls)
