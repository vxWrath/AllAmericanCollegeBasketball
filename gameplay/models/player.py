import enum
import math
import random
from typing import Any

from msgspec import Struct

from ..utils import round_to_quarter

__all__ = ["Year", "Position", "PlayerOrigin", "Player", "Recruit"]

OVERALL_WEIGHTS = {
    1: {  # Position.GUARD
        "inside_shot": 0.15,
        "outside_shot": 0.25,
        "interior_defense": 0.05,
        "perimeter_defense": 0.20,
        "athleticism": 0.10,
        "playmaking": 0.20,
        "rebounding": 0.05,
    },
    2: {  # Position.FORWARD
        "inside_shot": 0.20,
        "outside_shot": 0.20,
        "interior_defense": 0.15,
        "perimeter_defense": 0.15,
        "athleticism": 0.15,
        "playmaking": 0.10,
        "rebounding": 0.05,
    },
    3: {  # Position.POST
        "inside_shot": 0.30,
        "outside_shot": 0.05,
        "interior_defense": 0.25,
        "perimeter_defense": 0.05,
        "athleticism": 0.15,
        "playmaking": 0.05,
        "rebounding": 0.15,
    },
}


class Year(enum.IntEnum):
    FRESHMAN = 1
    SOPHOMORE = 2
    JUNIOR = 3
    SENIOR = 4


class Position(enum.IntEnum):
    GUARD = 1
    FORWARD = 2
    POST = 3


class PlayerOrigin(enum.StrEnum):
    HIGH_SCHOOL = "high_school"
    JUCO = "juco"
    LOWER_DIVISION = "lower_division"
    D1_TRANSFER = "d1_transfer"


class Player(Struct, kw_only=True, dict=True):
    id: int
    career_id: int
    team_id: int

    name: str
    position: Position
    year: Year
    origin: PlayerOrigin

    inside_shot: float  # dunks & layups
    outside_shot: float  # jump shots, mid-range, three, free throws
    interior_defense: float  # defense on inside shots
    perimeter_defense: float  # defense on outside shots
    athleticism: float  # rebounding, blocks
    playmaking: float  # dribbling, passing, court vision

    dev_rate: float  # multiplier for off-season attribute growth
    is_transferring: bool = False

    def __post_init__(self):
        self.cache: dict[str, Any] = {}

    @property
    def free_throw(self) -> float:
        if "free_throw" not in self.cache:
            self.cache["free_throw"] = round_to_quarter(
                self.outside_shot * 0.7 + self.inside_shot * 0.3
            )
        return self.cache["free_throw"]

    @property
    def rebounding(self) -> float:
        if "rebounding" not in self.cache:
            self.cache["rebounding"] = round_to_quarter(
                self.athleticism * 0.5 + self.interior_defense * 0.3 + self.playmaking * 0.2
            )
        return self.cache["rebounding"]

    def overall(self) -> float:
        if "overall" in self.cache:
            return self.cache["overall"]

        value = sum(
            getattr(self, skill) * weight
            for skill, weight in OVERALL_WEIGHTS[self.position.value].items()
        )

        value = round_to_quarter(value)
        self.cache["overall"] = value

        return value

    def stars(self) -> int:
        return max(1, min(5, math.ceil(self.overall() / 20)))

    def clear_cache(self) -> None:
        self.cache.clear()

    def __hash__(self) -> int:
        return self.id


class Recruit(Struct, kw_only=True, dict=True):
    id: int
    career_id: int
    name: str
    position: Position
    origin: PlayerOrigin
    estimated_stars: int | None = (
        None  # randomised from true rating; None until get_estimated_stars() is called
    )
    dev_rate: float = 0.0  # revealed after scouting

    inside_shot: float
    outside_shot: float
    interior_defense: float
    perimeter_defense: float
    athleticism: float
    playmaking: float

    scouted: bool = False
    committed_to: int | None = None  # team_id, or None if uncommitted

    def get_estimated_stars(self, rng: random.Random) -> int:
        if self.estimated_stars is None:
            offset = rng.choices([-1, 0, 1], weights=[0.2, 0.6, 0.2])[0]
            self.estimated_stars = max(1, min(5, self.stars() + offset))

        return self.estimated_stars

    def overall(self) -> float:
        rebounding = round_to_quarter(
            self.athleticism * 0.5 + self.interior_defense * 0.3 + self.playmaking * 0.2
        )

        attrs = {
            "inside_shot": self.inside_shot,
            "outside_shot": self.outside_shot,
            "interior_defense": self.interior_defense,
            "perimeter_defense": self.perimeter_defense,
            "athleticism": self.athleticism,
            "playmaking": self.playmaking,
            "rebounding": rebounding,
        }

        return round_to_quarter(
            sum(
                attrs[skill] * weight
                for skill, weight in OVERALL_WEIGHTS[self.position.value].items()
            )
        )

    def stars(self) -> int:
        return max(1, min(5, math.ceil(self.overall() / 20)))
