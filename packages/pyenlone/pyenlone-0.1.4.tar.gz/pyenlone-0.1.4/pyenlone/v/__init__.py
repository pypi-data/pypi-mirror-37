"""
Implements V methods for agent information. Constructor must be provide
with eihter
    apikey: an apikey from https://v.enl.one/apikey or
    token: an OAuth2 token with enough scopes for your use
as a keyword argument.

More detailed documentation on each method on
    https://v.enl.one/apikey and
    https://v.enl.one/oauth/clients
"""
from typing import List, Dict

from .._proxy import TokenProxy, KeyProxy, OpenProxy
from ._oauth import OAuthDelegate
from ._apikey import ApikeyDelegate
from .agent import Agent
from .detail_agent import DetailAgent
from .team import Team, TeamRole
from .team_member import TeamMember
from ..enloneexception import EnlOneException

__all__ = ["Agent", "DetailAgent", "Team", "TeamMember", "TeamRole", "V",
           "banned"]


def banned(gid: str):
    """
    Returns True iff the given google id correspond to an agent marked
    on V as banned.
    Open without Authentication.
    """
    return OpenProxy().get("/banned/" + gid)


class V:
    """
    Implements V methods for agent information. Constructor must be provided
    with eihter
        apikey: an apikey from https://v.enl.one/apikey or
        token: an OAuth2 token with enough scopes for your use
    as a keyword argument.

    More detailed documentation on each method on
        https://v.enl.one/apikey and
        https://v.enl.one/oauth/clients
    """
    _base_url = "https://v.enl.one"

    def __init__(self, cache=0, **kwargs):
        if "token" in kwargs:
            self._proxy = TokenProxy(self._base_url,
                                     kwargs["token"],
                                     cache=cache)
            self._delegate = OAuthDelegate(self._proxy)
        elif "apikey" in kwargs:
            self._proxy = KeyProxy(self._base_url,
                                   kwargs["apikey"],
                                   cache=cache)
            self._delegate = ApikeyDelegate(self._proxy)
        else:
            raise EnlOneException("You need to either provide token or apikey as keyword argument.")

    # v1 general endpoints
    def trust(self, enlid: str) -> Agent:
        """
        V-Points and V-Level could be queried by enlid.
        If you are VL2 or higher, you can also query V-Points and -Level using
        the Google+ ID instead of ENLID.
        Both API key and OAuth should work with this method.
        """
        api_result = self._proxy.get("/api/v1/agent/" + enlid + "/trust")
        api_result["enlid"] = enlid
        return Agent(api_result)

    def search(self, **kwargs) -> Agent:
        """
        Agents could be found by using this method. Several keywordarguments
        could be set to restrict the results.
        To receive some results either query or lat/lon must be set.
        Both API key and OAuth should work with this method.
        """
        api_result = self._proxy.get("/api/v1/search", params=kwargs)
        return [Agent(a) for a in api_result]

    def distance(self, enlid1: str, enlid2: str) -> List[Agent]:
        """
        Like in a profile, the connections between two agents can be queried
        using this method.
        If you are VL2 or higher, you can also use the Google+ ID
        instead of ENLID.
        Both API key and OAuth should work with this method.
        """
        api_result = self._proxy.get("/api/v1/agent/" + enlid1 + "/" + enlid2)
        return [Agent(a) for a in api_result["hops"]]

    def bulk_info(self, ids: List[str], telegramid=False, gid=False, array=False) -> List[Agent]:
        """
        To reduce the amount of requests, multiple agent could be queried
        using this method.
        The agents could be passed as an array of enlid.
        Both API key and OAuth should work with this method.
        """
        url = "/api/v1/bulk/agent/info"
        if telegramid:
            url += "/telegramid"
        if gid:
            url += "/gid"
        if array:
            url += "/array"
            api_result = self._proxy.post(url, ids)
            return [Agent(a) if a is not None else None for a in api_result]
        api_result = self._proxy.post(url, ids)
        return {enlid: (Agent(a) if a is not None else None)
                for (enlid, a) in api_result.items()}

    def location(self, enlid: str) -> Dict:
        """
        To retrive the location of an agent.
        Both API key and OAuth should work with this method.
        """
        return self._proxy.get("/api/v1/agent/" + enlid + "/location")

    def whoami(self) -> DetailAgent:
        """
        To retrieve the data of the owner of this apikey.
        This method is API key specific.
        """
        return self._delegate.whoami()
    # TODO: profile pictures

    # v2 endpoints
    def list_teams(self) -> List[Team]:
        """
        You can list all teams of the user by using this method.
        Extension in V2: This can handle teams where members can be assigned
        multiple roles.
        Both API key and OAuth should work with this method.
        """
        api_result = self._proxy.get("/api/v2/teams")
        return [Team(t) for t in api_result]

    def team_details(self, teamid) -> List[TeamMember]:
        """
        To retrieve a list of all members of a specific team.
        Extension in V2: This can handle teams where members can be assigned
        multiple roles.
        Note: You can only query your own teams! Since this API exposes much
        more data then the other APIs.
        Both API key and OAuth should work with this method.
        """
        api_result = self._proxy.get("/api/v2/teams/" + str(teamid))
        return [TeamMember(tm) for tm in api_result]

    # OAuth specifics
    def profile(self) -> Agent:
        """
        https://v.enl.one/oauth/clients
        This method is OAuth specific.
        """
        return self._delegate.profile()

    def googledata(self) -> Dict:
        """
        https://v.enl.one/oauth/clients
        This method is OAuth specific.
        """
        return self._delegate.googledata()

    def email(self) -> str:
        """
        This method is OAuth specific.
        """
        return self._delegate.email()

    def telegram(self) -> str:
        """
        https://v.enl.one/oauth/clients
        This method is OAuth specific.
        """
        return self._delegate.telegram()

    # Short-handers
    def search_one(self, **kwargs) -> Agent:
        """
        Short-hand to search for the first result.
        Both API key and OAuth should work with this method.
        """
        return self.search(**kwargs)[0]

    def is_ok(self, agent) -> bool:
        """
        DEPRECATED: use agent.is_ok instead.

        Given a search result, return true iff the agent is:
        verified, active, not quarantined, not blacklisted and not banned
        by nia.
        Both API key and OAuth should work with this method.
        """
        return agent.verified \
               and agent.active \
               and not agent.quarantine \
               and not agent.blacklisted \
               and not agent.banned_by_nia
