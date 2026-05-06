from typing import Any

__all__ = ["MISSING", "round_to_quarter"]

class _MissingSentinel:
    __slots__ = ()

    def __eq__(self, other) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self):
        return '...'


MISSING: Any = _MissingSentinel()

def round_to_quarter(value: float) -> float:
    """Round a float to the nearest quarter (0.25)."""
    return round(value * 4) / 4
