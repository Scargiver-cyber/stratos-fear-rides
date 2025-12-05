# stratosfear/settings.py
"""
Global configuration for Stratos-FEAR Rides.
Tweak these values to change game behavior without touching core code.
"""

# Total shared fuel pool for all spacecraft (units)
TOTAL_FUEL_POOL = 25000

# Terminal printing profiles
# You can add more profiles here if you want.
TERMINAL_PROFILES = {
    "normal": {
        "delay": 0.0005,   # fairly quick
        "jitter": 0.004,   # bouncy, but readable
    },
    "slow": {
        "delay": 0.0015,   # slower overall
        "jitter": 0.002,   # a bit smoother
    },
    "glitch": {
        "delay": 0.0002,   # very fast
        "jitter": 0.010,   # lots of chaos
    },
}

# Internal current profile name
_current_profile_name = "normal"


def get_terminal_timing():
    """Return (delay, jitter) for the currently selected terminal profile."""
    profile = TERMINAL_PROFILES[_current_profile_name]
    return profile["delay"], profile["jitter"]


def set_terminal_profile(name: str):
    """Set the active terminal profile by name."""
    global _current_profile_name
    if name not in TERMINAL_PROFILES:
        raise ValueError(f"Unknown terminal profile: {name}")
    _current_profile_name = name


def get_current_profile_name() -> str:
    """Get the name of the currently active terminal profile."""
    return _current_profile_name
