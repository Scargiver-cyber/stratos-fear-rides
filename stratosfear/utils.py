# stratosfear/utils.py
# Terminal effects, input helpers, and selection helpers

import time
import sys
import random

from .settings import get_terminal_timing

# ANSI colors for green terminal look
GREEN = "\033[92m"
RESET = "\033[0m"


def slow_print(text, delay=None, jitter=None, newline=True, beep=False):
    """Print text character-by-character like an old terminal.

    If delay or jitter are None, use the current terminal profile
    from settings.get_terminal_timing().
    """
    if delay is None or jitter is None:
        prof_delay, prof_jitter = get_terminal_timing()
        if delay is None:
            delay = prof_delay
        if jitter is None:
            jitter = prof_jitter

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(max(0.0, delay + random.uniform(0, jitter)))
    if newline:
        sys.stdout.write("\n")
        sys.stdout.flush()
    if beep:
        sys.stdout.write("\a")
        sys.stdout.flush()


def p(*args, **kwargs):
    """Replacement for print() that routes through slow_print().

    Prints in bright green (old terminal style).
    Supports basic print semantics: sep and end.
    """
    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", "\n")

    if args:
        text = sep.join(str(a) for a in args)
    else:
        text = ""

    newline = end.endswith("\n")
    slow_print(GREEN + text + RESET, newline=newline)


def ask_yes_no(prompt):
    """Ask a yes/no question and return True for yes, False for no."""
    while True:
        answer = input(f"{GREEN}{prompt} (y/n): {RESET}").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        p("  Please enter 'y' or 'n'.")


def ask_int(prompt, min_value=None, max_value=None):
    """Ask for an integer with optional min/max bounds."""
    while True:
        raw = input(f"{GREEN}{prompt}: {RESET}").strip()
        try:
            value = int(raw)
        except ValueError:
            p("  Please enter a valid integer.")
            continue

        if min_value is not None and value < min_value:
            p(f"  Value must be at least {min_value}.")
            continue
        if max_value is not None and value > max_value:
            p(f"  Value must be at most {max_value}.")
            continue
        return value


def choose_from_list(items, prompt):
    """Display a numbered list of items and let the user choose one.

    Returns the chosen item or None to cancel.
    """
    if not items:
        p("No options available.")
        return None

    while True:
        p("")
        p(prompt)
        p("-" * 40)
        for idx, item in enumerate(items, start=1):
            p(f"{idx}. {item}")
        p("0. Cancel / Done")

        choice = ask_int("Select an option", min_value=0, max_value=len(items))
        if choice == 0:
            return None
        return items[choice - 1]


def choose_crew_member(role, crew_list):
    """Let the user choose a crew member for a specific role."""
    prompt = f"Choose a {role} from the available crew"
    return choose_from_list(crew_list, prompt)


def assign_crew_interactively(spacecraft, captains, copilots, attendants, flight_ops):
    """Interactive helper to assign crew to a given spacecraft."""
    p("")
    p(f"--- ASSIGNING CREW FOR {spacecraft.name} ---")

    # Captain
    p("\nAssign a Captain:")
    captain = choose_crew_member("captain", captains)
    if captain:
        spacecraft.assign_crew_member(captain)

    # Copilot
    p("\nAssign a Copilot:")
    copilot = choose_crew_member("copilot", copilots)
    if copilot:
        spacecraft.assign_crew_member(copilot)

    # Attendant
    p("\nAssign a Flight Attendant:")
    attendant = choose_crew_member("attendant", attendants)
    if attendant:
        spacecraft.assign_crew_member(attendant)

    # Flight Ops
    p("\nAssign a Flight Ops crew member:")
    ops = choose_crew_member("flight ops crew member", flight_ops)
    if ops:
        spacecraft.assign_crew_member(ops)

    p(f"Completed crew assignment for {spacecraft.name}.\n")
