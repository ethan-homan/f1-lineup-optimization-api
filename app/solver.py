from typing import List, Dict, Any
from pulp import LpMaximize, LpProblem, lpSum, LpVariable, GLPK
from app.types import Player
from app.players import PlayerID, DriverID, ConstructorID
from app.config import CONSTRUCTOR_DRIVER_MAP, TURBO_DRIVER_THRESHOLD


def solve_lineup(
        players: Dict[PlayerID, Player],
        budget: float,
        allow_teammates: bool,
        include_override: List[PlayerID] = None,
        exclude_override: List[PlayerID] = None,
        no_turbo_override: List[DriverID] = None,
        turbo_override: DriverID = None,
        exclude_solutions: List[List[PlayerID]] = None,
) -> Dict[str, Any]:
    """
    This takes in information about players (drivers and constructors), budget, and optional configurations
    from the user to restrict the solution space and uses PuLP + GLPK to return the best lineup given
    the game's constraints and the user's configuration.

    :param players: A map of player ids and player objects with the score and cost information.
    :param budget: The budget available to spend.
    :param allow_teammates: If this is false then the solver won't select two drivers from the same team.
    :param include_override: Force solver to select drivers and constructors in this array.
    :param exclude_override: Force solver to not select drivers and constructors in this array.
    :param no_turbo_override: Force solver to not select drivers in this array as turbo drivers.
    :param turbo_override: Force solver to select this driver as the turbo driver.
    :param exclude_solutions: Force solver to not select this exact lineup.
    """

    model = LpProblem(name="fantasy.f1", sense=LpMaximize)
    team_vars = LpVariable.dicts("Players", list(players.keys()), 0, 1, cat="Integer")
    turbo_player_vars = LpVariable.dicts("Turbo", list(players.keys()), 0, 1, cat="Integer")

    # Define the objective to maximize as the sum of the scores of the players on the team, doubling
    # the score of the turbo driver.
    model += lpSum([players[i].score * (team_vars[i] + turbo_player_vars[i]) for i in team_vars])

    # Constrain the total cost by the budget available.
    model += lpSum([players[i].cost * team_vars[i] for i in team_vars]) <= budget

    # Constrain the solution to have 5 drivers and 1 constructor.
    model += lpSum([team_vars[i] for i in team_vars if isinstance(players[i].id, DriverID)]) == 5
    model += lpSum([team_vars[i] for i in team_vars if isinstance(players[i].id, ConstructorID)]) == 1

    # Optionally constrain the solution to exclude teammates.
    if not allow_teammates:
        for teammate1, teammate2 in CONSTRUCTOR_DRIVER_MAP.values():
            model += lpSum([team_vars[teammate1] + team_vars[teammate2]]) <= 1

    # Force the solver to include specified players
    if include_override:
        for player in include_override:
            model += team_vars[player] == 1

    # Force the solver to exclude specified players
    if exclude_override:
        for player in exclude_override:
            model += team_vars[player] == 0

    # Make sure we select exactly one turbo driver
    model += lpSum(turbo_player_vars) == 1

    # If we are taking the turbo driver as a given, just add them to the team.
    if turbo_override:
        model += turbo_player_vars[turbo_override] == 1
        model += team_vars[turbo_override] == 1
    else:
        # Otherwise, allow drivers under 20M who aren't in the no_turbo_override list to be selected as turbo drivers.
        for player in players.values():
            no_turbo_override = no_turbo_override or []
            if (
                    isinstance(player.id, DriverID) and
                    player.cost < TURBO_DRIVER_THRESHOLD and
                    player.id not in no_turbo_override
            ):
                model += turbo_player_vars[player.id] <= team_vars[player.id]
            else:
                model += turbo_player_vars[player.id] == 0

    # Constrain the solver by removing previously found solutions.
    # This is needed to find the top N solutions where N > 1.
    if exclude_solutions:
        for solution in exclude_solutions:
            model += lpSum([team_vars[i] for i in solution]) <= 5

    model.solve(solver=GLPK(msg=False))

    assert model.status == 1, f"{model.status}"

    drivers = []
    turbo = None
    constructor = None
    for v in model.variables():
        if v.varValue > 0:
            raw_id = v.name.split(".")[-1]
            if "ConstructorID" in v.name:
                constructor = ConstructorID(raw_id)
            elif "Turbo" in v.name:
                turbo = DriverID(raw_id)
            else:
                drivers.append(DriverID(raw_id))

    team = drivers + [constructor]
    return {
        "drivers": drivers,
        "constructor": constructor,
        "turbo": turbo,
        "cost": sum([players[i].cost for i in team]),
        "score": sum([players[i].score for i in team]),
    }


def solve_top_lineups(
    n: int,
    players: Dict[PlayerID, Player],
    budget: float,
    allow_teammates: bool,
    include_override: List[PlayerID] = None,
    exclude_override: List[PlayerID] = None,
    no_turbo_override: List[DriverID] = None,
    turbo_override: DriverID = None,
):
    """
    This takes in information about players (drivers and constructors), budget, and optional configurations
    from the user to restrict the solution space and uses PuLP + GLPK to return the N best lineups given
    the game's constraints and the user's configuration.

    :param n: the number of solutions to return.
    :param players: A map of player ids and player objects with the score and cost information.
    :param budget: The budget available to spend.
    :param allow_teammates: If this is false then the solver won't select two drivers from the same team.
    :param include_override: Force solver to select drivers and constructors in this array.
    :param exclude_override: Force solver to not select drivers and constructors in this array.
    :param no_turbo_override: Force solver to not select drivers in this array as turbo drivers.
    :param turbo_override: Force solver to select this driver as the turbo driver.
    """

    solutions = []
    for i in range(n):
        if solutions:
            exclude_solutions = []
            for solution in solutions:
                exclude_solutions.append(
                    solution["drivers"] + [solution["constructor"]]
                )
        else:
            exclude_solutions = None
        solutions.append(
            solve_lineup(
                players,
                budget=budget,
                allow_teammates=allow_teammates,
                exclude_solutions=exclude_solutions,
                include_override=include_override,
                exclude_override=exclude_override,
                no_turbo_override=no_turbo_override,
                turbo_override=turbo_override,
            )
        )
    return solutions
