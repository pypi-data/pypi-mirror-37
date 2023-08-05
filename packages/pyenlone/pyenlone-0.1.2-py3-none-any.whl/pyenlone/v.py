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
from ._proxy import TokenProxy, KeyProxy, OpenProxy
from ._oauth import VOAuth
from .enloneexception import EnlOneException


def banned(gid):
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
            self._oauth = VOAuth(self._proxy)
        elif "apikey" in kwargs:
            self._proxy = KeyProxy(self._base_url,
                                   kwargs["apikey"],
                                   cache=cache)
        else:
            raise EnlOneException("You need to either provide token or apikey as keyword argument.")

    # v1 general endpoints
    def trust(self, enlid):
        """
        V-Points and V-Level could be queried by enlid.
        If you are VL2 or higher, you can also query V-Points and -Level using
        the Google+ ID instead of ENLID.
        Both API key and OAuth should work with this method.
        """
        return self._proxy.get("/api/v1/agent/" + enlid + "/trust")

    def search(self, **kwargs):
        """
        Agents could be found by using this method. Several keywordarguments
        could be set to restrict the results.
        To receive some results either query or lat/lon must be set.
        Both API key and OAuth should work with this method.
        """
        return self._proxy.get("/api/v1/search", params=kwargs)

    def distance(self, enlid1, enlid2):
        """
        Like in a profile, the connections between two agents can be queried
        using this method.
        If you are VL2 or higher, you can also use the Google+ ID
        instead of ENLID.
        Both API key and OAuth should work with this method.
        """
        return self._proxy.get("/api/v1/agent/" + enlid1 + "/" + enlid2).hops

    def bulk_info(self, ids, telegramid=False, gid=False, array=False):
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
        return self._proxy.post(url, ids)

    def location(self, enlid):
        """
        To retrive the location of an agent.
        Both API key and OAuth should work with this method.
        """
        return self._proxy.get("/api/v1/agent/" + enlid + "/location")

    def whoami(self):
        """
        To retrieve the data of the owner of this apikey.
        This method is API key specific.
        """
        return self._proxy.get("/api/v1/whoami")
    # TODO: profile pictures

    # v2 endpoints
    def list_teams(self):
        """
        You can list all teams of the user by using this method.
        Extension in V2: This can handle teams where members can be assigned
        multiple roles.
        Both API key and OAuth should work with this method.
        """
        return self._proxy.get("/api/v2/teams", )

    def team_details(self, teamid):
        """
        To retrieve a list of all members of a specific team.
        Extension in V2: This can handle teams where members can be assigned
        multiple roles.
        Note: You can only query your own teams! Since this API exposes much
        more data then the other APIs.
        Both API key and OAuth should work with this method.
        """
        return self._proxy.get("/api/v2/teams/" + str(teamid))

    # OAuth specifics
    def profile(self):
        """
        https://v.enl.one/oauth/clients
        This method is OAuth specific.
        """
        return self._oauth.profile()

    def googledata(self):
        """
        https://v.enl.one/oauth/clients
        This method is OAuth specific.
        """
        return self._oauth.googledata()

    def email(self):
        """
        This method is OAuth specific.
        """
        return self._oauth.email()

    def telegram(self):
        """
        https://v.enl.one/oauth/clients
        This method is OAuth specific.
        """
        return self._oauth.telegram()

    # Short-handers
    def search_one(self, **kwargs):
        """
        Short-hand to search for the first result.
        Both API key and OAuth should work with this method.
        """
        return self.search(**kwargs)[0]

    def is_ok(self, agent):
        """
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
