from urllib import request
from typing import Optional
from urllib.error import HTTPError, URLError


class ContentFetcher:

    def __init__(self, user_agents):
        self.user_agents = user_agents
        self.user_agent_index = 0

    def get_user_agent(self) -> Optional[str]:
        if len(self.user_agents) == 0:
            return None
        user_agent = self.user_agents[self.user_agent_index]
        self.user_agent_index = (self.user_agent_index + 1) % len(self.user_agents)
        return user_agent

    def retrieve_page(self, url: str) -> str:
        url_request = request.Request(url)
        user_agent = self.get_user_agent()
        if user_agent is not None:
            url_request.add_header("User-Agent", user_agent)
        try:
            return request.urlopen(url_request).read().decode("utf-8")
        except HTTPError:
            return ""
        except URLError:
            return ""
