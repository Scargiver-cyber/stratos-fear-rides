# stratosfear/__main__.py
from .utils import p, GREEN, RESET
from .simulation import run_simulation
from .settings import (
    TERMINAL_PROFILES,
    set_terminal_profile,
    get_current_profile_name,
)


def change_terminal_mode():
    p("\n--- TERMINAL DISPLAY MODES ---")

    profile_names = list(TERMINAL_PROFILES.keys())
    current = get_current_profile_name()

    for idx, name in enumerate(profile_names, start=1):
        cfg = TERMINAL_PROFILES[name]
        marker = " (current)" if name == current else ""
        p(
            f"{idx}. {name}{marker} "
            f"- delay={cfg['delay']}  jitter={cfg['jitter']}"
        )
    p("0. Cancel")

    raw = input(f"{GREEN}Select a profile: {RESET}").strip()
    if raw == "0":
        return

    try:
        sel = int(raw)
    except ValueError:
        p("Invalid selection.")
        return

    if 1 <= sel <= len(profile_names):
        chosen = profile_names[sel - 1]
        set_terminal_profile(chosen)
        p(f"Terminal profile set to '{chosen}'.")
    else:
        p("Invalid selection.")


def main():
    p("\n" + "=" * 60)
    p("        STRATOS-FEAR RIDES - MISSION CONTROL")
    p("=" * 60)

    director_name = input(
        f"{GREEN}Mission Director, please enter your name: {RESET}"
    ).strip() or "Director"

    while True:
        p("\n" + "=" * 60)
        p("   STRATOS-FEAR RIDES - MISSION CONTROL MAIN MENU")
        p("=" * 60)
        p("1. Run Full Simulation (planning + booking + launch)")
        p("2. Quick Status Only (no booking or launches)")
        p("3. Exit Program")
        p("4. Change terminal display mode")
        p("=" * 60)

        choice = input(f"{GREEN}Enter selection: {RESET}").strip()

        if choice == "1":
            run_simulation(director_name, quick=False)
        elif choice == "2":
            run_simulation(director_name, quick=True)
        elif choice == "3":
            p("\nExiting Mission Control. Safe travels, Director!\n")
            break
        elif choice == "4":
            change_terminal_mode()
        else:
            p("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
