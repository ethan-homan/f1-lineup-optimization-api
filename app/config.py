from app.players import DriverID, ConstructorID, PlayerID
from typing import Dict, Tuple

# Drivers above this threshold are not allowed to be selected as turbo drivers
TURBO_DRIVER_THRESHOLD = 20

# TODO: Throw this in a DB and setup a scraper to keep it up to date
COSTS: Dict[PlayerID, float] = {
 DriverID.Verstappen: 30.5,
 DriverID.Hamilton: 31.0,
 DriverID.Perez: 17.5,
 DriverID.Norris: 16.0,
 DriverID.Leclerc: 18.0,
 DriverID.Bottas: 9.0,
 DriverID.Sainz: 17.0,
 DriverID.Gasly: 13.5,
 DriverID.Vettel: 11.5,
 DriverID.Ricciardo: 14.5,
 DriverID.Alonso: 12.5,
 DriverID.Ocon: 12.0,
 DriverID.Stroll: 9.5,
 DriverID.Tsunoda: 8.5,
 DriverID.Albon: 7.5,
 DriverID.Zhou: 8.0,
 DriverID.Schumacher: 6.5,
 DriverID.Russell: 24.0,
 DriverID.Magnussen: 5.5,
 DriverID.Latifi: 7.0,
 ConstructorID.Redbull: 32.5,
 ConstructorID.Mercedes: 34.5,
 ConstructorID.McLaren: 18.5,
 ConstructorID.Ferrari: 25.0,
 ConstructorID.AstonMartin: 11.5,
 ConstructorID.AlphaTauri: 10.5,
 ConstructorID.Alpine: 14.0,
 ConstructorID.AlfaRomeo: 8.0,
 ConstructorID.Haas: 6.0,
 ConstructorID.Williams: 7.0
}

CONSTRUCTOR_DRIVER_MAP: Dict[ConstructorID, Tuple[DriverID, DriverID]] = {
    ConstructorID.Redbull:          (DriverID.Verstappen, DriverID.Perez),
    ConstructorID.Mercedes:         (DriverID.Hamilton, DriverID.Russell),
    ConstructorID.McLaren:          (DriverID.Norris, DriverID.Ricciardo),
    ConstructorID.Ferrari:          (DriverID.Leclerc, DriverID.Sainz),
    ConstructorID.AstonMartin:      (DriverID.Vettel, DriverID.Stroll),
    ConstructorID.AlphaTauri:       (DriverID.Gasly, DriverID.Tsunoda),
    ConstructorID.Alpine:           (DriverID.Alonso, DriverID.Ocon),
    ConstructorID.AlfaRomeo:        (DriverID.Bottas, DriverID.Zhou),
    ConstructorID.Haas:             (DriverID.Schumacher, DriverID.Magnussen),
    ConstructorID.Williams:         (DriverID.Albon, DriverID.Latifi),
}
