from typing import Any
from pydantic import BaseModel


class GameState(BaseModel):
    field: list[list[bool]]
    next: list[list[bool]]
    score: int
    higth_score: int
    level: int
    speed: int
    pause: bool
    shift_new_row: int
    cycle: int
    car: Any = None


class UserEnvironment(BaseModel):
    game_websocket: Any
    player_websocket: Any
    client_id: int
    game_state: Any


class Id(BaseModel):
    id: int