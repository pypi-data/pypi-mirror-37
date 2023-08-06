from typing import List
from .detail_agent import DetailAgent
from .team import TeamRole


class TeamMember(DetailAgent):
    """
    A member of one of your teams.
    """
    def __init__(self, api_result):
        super().__init__(api_result)
        self._admin = api_result["admin"]
        self._roles = [TeamRole(r["id"], r["name"])
                       for r in api_result["roles"]]
        self._distance = api_result["distance"]

    @property
    def admin(self):
        return self._admin

    @property
    def roles(self) -> List[TeamRole]:
        return self._roles
