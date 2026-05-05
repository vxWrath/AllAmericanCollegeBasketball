__all__ = ["round_to_quarter"]

def round_to_quarter(value: float) -> float:
    """Round a float to the nearest quarter (0.25)."""
    return round(value * 4) / 4
