from enum import Enum
from typing import List


class RoleType(Enum):
    PLANNER = 0
    OPERATOR = 1
    LINKER = 2
    KEYFARMING = 3
    CLEANER = 4
    FIELD_AGENT = 5
    ITEM_SPONSOR = 6
    KEY_TRANSPORT = 7
    RECHARGING = 8
    SOFTWARE_SUPPORT = 9
    ANOMALY_TL = 10
    TEAM_LEAD = 11
    OTHER = 99


class TeamRole:
    def __init__(self, id, name):
        self._id = id
        role_translation = {
            "Planner": RoleType.PLANNER,
            "Operator": RoleType.OPERATOR,
            "Linker": RoleType.LINKER,
            "Keyfarming": RoleType.KEYFARMING,
            "Cleaner": RoleType.CLEANER,
            "Field Agent": RoleType.FIELD_AGENT,
            "Item Sponser": RoleType.ITEM_SPONSOR,
            "Key Transport": RoleType.KEY_TRANSPORT,
            "Recharging": RoleType.RECHARGING,
            "Software Support": RoleType.SOFTWARE_SUPPORT,
            "Anomaly TL": RoleType.ANOMALY_TL,
            "Team Lead": RoleType.TEAM_LEAD,
            "Other": RoleType.OTHER
        }
        self._name = role_translation[name]

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

class Team:
    def __init__(self, api_result):
        self._teamid = api_result["teamid"]
        self._team = api_result["team"]

        self._roles = [TeamRole(r["id"], r["name"])
                       for r in api_result["roles"]]

    @property
    def teamid(self) -> int:
        return self._teamid

    @property
    def team(self) -> str:
        return self._team

    @property
    def roles(self) -> List[TeamRole]:
        return self._roles
