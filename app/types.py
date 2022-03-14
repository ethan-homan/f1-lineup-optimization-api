from pydantic import BaseModel
from enum import Enum
from typing import Optional, List, NamedTuple
from app.players import DriverID, PlayerID


class Override(Enum):
    """
    Specifies the types of user overrides we can accept:
        INCLUDE: Force a Driver or Constructor to be included in the solution
        EXCLUDE: Force a Driver or Constructor to be excluded from the solution
        TURBO: Force a Driver to be selected as the turbo driver
        NO_TURBO: Force a Driver to not be selected as the turbo driver
    """
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"
    TURBO = "TURBO"
    NO_TURBO = "NO_TURBO"


class PlayerOverride(BaseModel):
    id: PlayerID
    override: Override


class DriverScore(BaseModel):
    id: DriverID
    score: float


class UserModelSpec(BaseModel):
    driver_scores: List[DriverScore]
    budget: float
    allow_teammates: bool = True
    overrides: Optional[List[PlayerOverride]]


class Player(NamedTuple):
    id: PlayerID
    score: float
    cost: float
