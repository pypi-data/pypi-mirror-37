"""
Implementation of oauth specific endpoints.
"""


class VOAuth:
    """
    Implementation of oauth specific endpoints.
    """
    def __init__(self, proxy):
        self._proxy = proxy

    def profile(self):
        return self._proxy.get("/api/v1/profile")

    def googledata(self):
        return self._proxy.get("/api/v1/googledata")

    def email(self):
        return self._proxy.get("/api/v1/email")

    def telegram(self):
        return self._proxy.get("/api/v1/telegram")
