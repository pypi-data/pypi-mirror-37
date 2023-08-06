class Agent:
    """
    Basic agent data.
    It's ok to make this public, I think.
    """
    def __init__(self, api_result):
        self._enlid = api_result["enlid"]
        self._agent = api_result["agent"]
        self._vlevel = api_result["vlevel"]
        self._vpoints = api_result["vpoints"]
        self._verified = api_result["verified"]
        self._active = api_result["active"]
        self._flagged = api_result["flagged"]
        self._quarantine = api_result["quarantine"]
        self._blacklisted = api_result["blacklisted"]
        self._cellid = api_result["cellid"]
        self._banned_by_nia = api_result["banned_by_nia"]

    @property
    def enlid(self) -> str:
        return self._enlid

    @property
    def agent(self) -> str:
        return self._agent

    @property
    def vlevel(self) -> int:
        return self._vlevel

    @property
    def vpoints(self) -> int:
        return self._vpoints

    @property
    def verified(self) -> bool:
        return self._verified

    @property
    def active(self) -> bool:
        return self._active

    @property
    def flagged(self) -> bool:
        return self._flagged

    @property
    def quarantine(self) -> bool:
        return self._quarantine

    @property
    def blacklisted(self) -> bool:
        return self._blacklisted

    @property
    def banned_by_nia(self) -> bool:
        return self._banned_by_nia

    @property
    def cellid(self) -> str:
        return self._cellid

    @property
    def profile_link(self) -> str:
        return "https://v.enl.one/profile/" + self.enlid
