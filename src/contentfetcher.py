from urllib import request
from typing import Optional, List
from urllib.error import HTTPError, URLError


class ContentFetcher:
    """
    Responsible for fetching content from a given URL.
    """
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

    def retrieve_page(self, url: str) -> str:
        """
        Attempts to fetch the web page at the provided url, returning its contents as a string.
        :param url: the url to fetch from.
        :return: contents of fetched web page, or empty string if fetching failed
        """
        url_request = request.Request(url)
        user_agent = self.get_next_user_agent()
        if user_agent is not None:
            url_request.add_header("User-Agent", user_agent)
        url_request.add_header("Accept", "text/html")
        try:
            return request.urlopen(url_request).read().decode("utf-8", "ignore")
        except (HTTPError, URLError, UnicodeDecodeError) as e:
            print(e)
            return ""

