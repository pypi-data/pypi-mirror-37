from .agent import Agent
from .detail_agent import DetailAgent
from ..enloneexception import EnlOneException


class ApikeyDelegate:
    """
    Implementation of oauth specific endpoints.
    """
    def __init__(self, proxy):
        self._proxy = proxy

    def profile(self) -> Agent:
        return self.whoami()

    def googledata(self):
        raise EnlOneException("This method is only available using OAuth token")

    def email(self):
        return self._proxy.get("/api/v1/whoami")["email"]

    def telegram(self):
        return self._proxy.get("/api/v1/whoami")["telegram"]

    def whoami(self):
        return DetailAgent(self._proxy.get("/api/v1/whoami"))
