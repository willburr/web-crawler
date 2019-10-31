from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from typing import Optional, List, Tuple
import gzip
import zlib


def decompress_gzip(content: bytes) -> bytes:
    """
    Decompress content compressed with gzip
    :param content: content to decompress
    :return:
    """
    try:
        return gzip.decompress(content)
    except OSError:
        return b''


def decompress_deflate(content: bytes) -> bytes:
    """
    Decompress content compressed with deflate
    :param content: content to decompress
    :return:
    """
    return zlib.decompress(content)


class ContentFetcher:
    """
    Responsible for fetching content from a given URL.
    """

    decompressors = {
        "gzip": decompress_gzip,
        "deflate": decompress_deflate
    }

    def __init__(self, user_agents: List[str]):
        """
        :param user_agents: list of user agent strings to cycle through for request headers
        """
        self.user_agents = user_agents
        self.user_agent_index = 0

    def get_next_user_agent(self) -> Optional[str]:
        """
        Retrieves the next user agent. The code will cycle through the provided user agents
        sequentially.
        :return: a string representing a user agent, or None if no user agents were provided
        """
        if len(self.user_agents) == 0:
            return None
        user_agent = self.user_agents[self.user_agent_index]
        self.user_agent_index = (self.user_agent_index + 1) % len(self.user_agents)
        return user_agent

    def decompress_content(self, content: bytes, encoding: str) -> bytes:
        """
        Attempt to decompress the content given the encoding
        :param content: content to decompress
        :param encoding: encoding as extracted from response header
        :return: decompressed bytes if successful, empty byte string if not
        """
        if encoding in self.decompressors:
            return self.decompressors[encoding](content)
        return b''

    def retrieve_page(self, url: str) -> str:
        """
        Attempts to fetch the web page at the provided url, returning its contents as a string.
        :param url: the url to fetch from.
        :return: contents of fetched web page, or empty string if fetching failed
        """
        request = self.construct_request(url)
        try:
            response = urlopen(request)
            return self.handle_response(response.getheaders(), response.read())
        except (HTTPError, URLError) as e:
            print(e)
            return ""

    def construct_request(self, url: str) -> Request:
        """
        Build the HTTP request for the URL given
        :param url: url to request as a string
        :return: an urllib Request object
        """
        url_request = Request(url)
        user_agent = self.get_next_user_agent()
        if user_agent is not None:
            url_request.add_header("User-Agent", user_agent)
        url_request.add_header("Accept", "text/html")
        url_request.add_header("Accept-Encoding", "gzip, deflate")
        return url_request

    def handle_response(self, headers: List[Tuple], content: bytes) -> str:
        """
        Handle the HTTP response, including any encoding and compression
        :param headers: list of tuples representing the response headers
        :param content: bytes of content
        :return: string containing the decoded, decompressed page contents
        """
        for header in headers:
            if header[0] == "Content-Encoding":
                encoding = header[1]
                if encoding is not None:
                    content = self.decompress_content(content, encoding)
        return content.decode("utf-8", "ignore")
