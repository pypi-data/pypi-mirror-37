from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple

from .operation import Operation
from .task import Task
from .message import Message
from .grant import Grant
from .._proxy import TokenProxy, KeyProxy


__all__ = [Operation, Task, Message, Grant]


class OpType(Enum):
    FIELD = 0
    FIELD_DEFENDE = 1
    AREA = 2
    LINKSTAR = 3
    LINKART = 4
    OTHER = 5


class TaskType(Enum):
    DESRTOY = 1
    CAPTRURE = 2
    FLIP = 4
    LINK = 8
    KEYFARM = 9
    MEET = 10
    RECHARGE = 11
    UPGRADE = 12
    OTHER = 99

Box = Tuple[char, char, char, char]
    
class Tasks:
    def __init__(self, apikey=None: str, voauth=None: str, rocks=None: str, enlio=None:str, cache=0: int):
        self._proxy = TokenProxy("https://tasks.enl.one", token, cache=cache)
        pass

    def new_operation(name: str, optype: OpType, box: OpBox) -> Operation:
        pass

    def get_operations(**kwargs):
        pass

    def search_operations(lat: float, lon: float, km: float) -> List(Operation):
        pass

    def get_tasks(**kwargs):
        pass
    
    def search_tasks(lat: float, lon: float, km: float) -> List(Task):
        pass
    
    
