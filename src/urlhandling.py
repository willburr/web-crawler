import re
from urllib.parse import urljoin, urlparse, urlsplit


def is_http_url(url: str) -> bool:
    """
    Returns true if the URL is considered to be an absolute url with a http or https prefix.
    Uses a simple regex check on the start of the url. Then check the rest of the structure
    using urlparse.
    :param url: url to check
    :return: a boolean
    """
    http_regex = 'https?://'
    http_pattern = re.compile(http_regex)
    if http_pattern.search(url, 0, len(http_regex) - 1) is None:
        return False
    return urlparse(url).netloc != ''


def is_relative_url(url: str) -> bool:
    """
    Returns true if URL is considered to be a relative url.
    Uses urlparse to see if the url is just a path.
    :param url:
    :return:
    """
    return urlparse(url).path == url


def construct_absolute_url(absolute_url: str, relative_url: str) -> str:
    """
    Constructs an absolute url using an absolute url and a relative url for the same site.
    :param absolute_url: the absolute url
    :param relative_url: the relative url (path)
    :return: an absolute url
    """
    return urljoin(absolute_url, relative_url)


def normalise_url(url: str) -> str:
    """
    Normalises the url by converting scheme to lower case and dropping empty components.
    Used so that we do not visit the same url twice.
    :param url: url to normalise
    :return: a normalised string
    """
    return urlsplit(url).geturl()
