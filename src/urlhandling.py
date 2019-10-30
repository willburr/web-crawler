import re
from urllib.parse import urljoin, urlparse, urlsplit


def is_http_url(url: str) -> bool:
    http_regex = 'https?://'
    http_pattern = re.compile(http_regex)
    return http_pattern.search(url, 0, len(http_regex) - 1) is not None


def is_relative_url(url: str) -> bool:
    return urlparse(url).path == url


def construct_absolute_url(absolute_url: str, relative_url: str) -> str:
    return urljoin(absolute_url, relative_url)

def normalise_url(url: str) -> str:
    return urlsplit(url).geturl()
