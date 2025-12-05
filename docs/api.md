# API Reference

## Package: `stratosfear`

### `run_simulation(director_name: str, quick: bool = False)`

Entry point for running a simulation programmatically.

- `director_name`: Name shown in prompts and messages.
- `quick`: If `True`, skips passenger booking and launch sequence.

### `TOTAL_FUEL_POOL`

Integer constant representing the total shared fuel available at the depot.

### Terminal settings

- `TERMINAL_PROFILES`: Dict of terminal timing profiles.
- `get_terminal_timing()`: Returns `(delay, jitter)` for the active profile.
- `set_terminal_profile(name)`: Switch active profile.
- `get_current_profile_name()`: Get name of the active profile.

### Core classes

- `CrewMember(name, role, experience=0)`
- `Spacecraft(name, seats, fuel_capacity)`
- `Mission(name, destination, fuel_required)`
