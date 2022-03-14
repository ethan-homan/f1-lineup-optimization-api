from typing import List, Dict
from app.types import Player
from app.players import PlayerID, ConstructorID
from app.types import DriverScore, PlayerOverride, Override
from app.config import COSTS, CONSTRUCTOR_DRIVER_MAP


class LineupOptimizationModelSpec:

    def __init__(
            self,
            driver_scores: List[DriverScore],
            budget: float,
            allow_teammates: bool,
            overrides: List[PlayerOverride] = None,
    ):
        self.budget = budget
        self.allow_teammates = allow_teammates

        self.player_scores: Dict[PlayerID, Player] = {
            i.id: Player(i.id, i.score, COSTS[i.id]) for i in driver_scores
        }

        for constructor_id in ConstructorID:
            driver_id_1, driver_id_2 = CONSTRUCTOR_DRIVER_MAP[constructor_id]
            constructor_score = self.player_scores[driver_id_1].score + self.player_scores[driver_id_2].score
            self.player_scores[constructor_id] = Player(
                constructor_id,
                constructor_score,
                COSTS[constructor_id],
            )

        self.turbo_override = None
        self.no_turbo_override = None
        self.exclude_override = None
        self.include_override = None

        if overrides:
            # TODO: Add more validation here, there are a lot of ways to define invalid configurations through overrides
            include_override = [p.id for p in overrides if p.override == Override.INCLUDE]
            if len(include_override) > 0:
                self.include_override = include_override

            exclude_override = [p.id for p in overrides if p.override == Override.EXCLUDE]
            if len(exclude_override) > 0:
                self.exclude_override = exclude_override

            no_turbo_override = [p.id for p in overrides if p.override == Override.NO_TURBO]
            if len(no_turbo_override) > 0:
                self.no_turbo_override = no_turbo_override

            turbo_override = [p.id for p in overrides if p.override == Override.TURBO]
            if len(turbo_override) == 0:
                pass
            elif len(turbo_override) == 1:
                self.turbo_override = turbo_override[0]
            else:
                raise Exception("Cannot specify multiple turbo drivers")
