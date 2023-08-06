from .agent import Agent


class DetailAgent(Agent):
    """
    Agents with sensitive data. Not ok to make any of this public.
    """
    def __init__(self, api_result):
        super().__init__(api_result)
        self._telegram = api_result["telegram"]
        self._telegramid = api_result["telegramid"]
        self._email = api_result["email"]
        self._gid = api_result["gid"]
        self._lat = api_result["lat"]
        self._lon = api_result["lon"]

    @property
    def telegram(self) -> str:
        return self._telegram

    @property
    def telegramid(self) -> int:
        return self._telegramid

    @property
    def email(self) -> str:
        return self._email

    @property
    def gid(self) -> str:
        return self._gid
