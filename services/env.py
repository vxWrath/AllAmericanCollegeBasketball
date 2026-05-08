import os
import sys
from typing import Any, Optional

from .logger import get_logger

__all__ = ["get_env", "is_production"]

logger = get_logger("env")

def get_env(name: str, default: Optional[Any]=None) -> str:
    value = os.getenv(key=name, default=default)

    if value is None:
        logger.fatal(f"Environment variable '{name}' is not set.")
        sys.exit(1)
        
    return value

def is_production() -> bool:
    return get_env("PROD", "False") == "True"