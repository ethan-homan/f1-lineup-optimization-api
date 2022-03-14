"""
Drivers and constructors are usually static most of the season, hard coding these for now should be fine and these
enums are useful in a few places.
"""

from enum import Enum
from typing import Union


class ConstructorID(Enum):
    Redbull = "Redbull"
    Mercedes = "Mercedes"
    McLaren = "McLaren"
    Ferrari = "Ferrari"
    AstonMartin = "AstonMartin"
    AlphaTauri = "AlphaTauri"
    Alpine = "Alpine"
    AlfaRomeo = "AlfaRomeo"
    Haas = "Haas"
    Williams = "Williams"


class DriverID(Enum):
    Verstappen = "Verstappen"
    Hamilton = "Hamilton"
    Perez = "Perez"
    Norris = "Norris"
    Leclerc = "Leclerc"
    Bottas = "Bottas"
    Sainz = "Sainz"
    Gasly = "Gasly"
    Vettel = "Vettel"
    Ricciardo = "Ricciardo"
    Alonso = "Alonso"
    Ocon = "Ocon"
    Stroll = "Stroll"
    Tsunoda = "Tsunoda"
    Albon = "Albon"
    Zhou = "Zhou"
    Schumacher = "Schumacher"
    Russell = "Russell"
    Magnussen = "Magnussen"
    Latifi = "Latifi"


PlayerID = Union[DriverID, ConstructorID]
