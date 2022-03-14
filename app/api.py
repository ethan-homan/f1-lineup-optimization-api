import logging
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from app.types import UserModelSpec
from app.solver import solve_top_lineups
from app.model_spec import LineupOptimizationModelSpec

gunicorn_error_logger = logging.getLogger("gunicorn.error")
logging.root.handlers.extend(gunicorn_error_logger.handlers)
logging.root.setLevel(gunicorn_error_logger.level)

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return jsonable_encoder(
        dict(status="ok")
    )


@router.post("/optimize-lineup/")
async def optimize_lineup(model: UserModelSpec):
    model = LineupOptimizationModelSpec(**dict(model))
    solutions = solve_top_lineups(
        5,
        players=model.player_scores,
        budget=model.budget,
        allow_teammates=model.allow_teammates,
        include_override=model.include_override,
        exclude_override=model.exclude_override,
        turbo_override=model.turbo_override,
        no_turbo_override=model.no_turbo_override,
    )
    return jsonable_encoder(
        solutions
    )
