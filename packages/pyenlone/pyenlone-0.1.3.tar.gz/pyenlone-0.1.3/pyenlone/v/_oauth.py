"""
Implementation of oauth specific endpoints.
"""
from .agent import Agent
from ..enloneexception import EnlOneException


class OAuthDelegate:
    """
    Implementation of oauth specific endpoints.
    """
    def __init__(self, proxy):
        self._proxy = proxy

    def profile(self):
        return Agent(self._proxy.get("/api/v1/profile"))

    def googledata(self):
        return self._proxy.get("/api/v1/googledata")

    def email(self):
        return self._proxy.get("/api/v1/email")["email"]

    def telegram(self):
        return self._proxy.get("/api/v1/telegram")["telegram"]

    def whoami(self):
        raise EnlOneException("This method is only available using API Key")
