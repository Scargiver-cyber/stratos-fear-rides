# stratosfear/__init__.py
"""Stratos-FEAR Rides - Space Tourism Simulation Package"""

from .simulation import run_simulation
from .settings import (
    TOTAL_FUEL_POOL,
    TERMINAL_PROFILES,
    get_terminal_timing,
    set_terminal_profile,
    get_current_profile_name,
)

__all__ = [
    "run_simulation",
    "TOTAL_FUEL_POOL",
    "TERMINAL_PROFILES",
    "get_terminal_timing",
    "set_terminal_profile",
    "get_current_profile_name",
]
