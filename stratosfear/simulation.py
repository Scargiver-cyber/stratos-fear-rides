# stratosfear/simulation.py
# Full mission planning + launch simulation logic

from .utils import (
    p,
    ask_yes_no,
    ask_int,
    choose_from_list,
    assign_crew_interactively,
)
from .classes import CrewMember, Spacecraft, Mission
from .settings import TOTAL_FUEL_POOL


def run_simulation(director_name, quick=False):
    """Run one full mission planning + launch simulation.

    quick = False  -> full flow: booking + launch sequence.
    quick = True   -> status-only: NO booking, NO launches, just setup and reports.
    """

    mode_label = "QUICK STATUS MODE" if quick else "FULL SIMULATION"
    p(f"\n[{mode_label}] Welcome, {director_name}! Let's prepare today's missions.\n")

    # ------------------------------------------------------------------
    # CREATE CREW MEMBER OBJECTS
    # ------------------------------------------------------------------
    p("--- INITIALIZING CREW ROSTER ---")

    captains = [
        CrewMember("Zaphod Beeblebrox", "captain", 15),
        CrewMember("Han Solo", "captain", 20),
        CrewMember("Malcolm Reynolds", "captain", 12),
        CrewMember("Jean-Luc Picard", "captain", 25),
        CrewMember("Ellen Ripley", "captain", 18),
    ]

    # Copilots
    copilots = [
        CrewMember("Data", "copilot", 10),
        CrewMember("TARS", "copilot", 8),
        CrewMember("K-2SO", "copilot", 6),
        CrewMember("Marvin the Paranoid Android", "copilot", 100),
        CrewMember("C-3PO", "copilot", 50),
    ]

    # Flight Attendants
    attendants = [
        CrewMember("Trillian", "attendant", 5),
        CrewMember("Leela", "attendant", 7),
        CrewMember("Kaylee Frye", "attendant", 4),
        CrewMember("Nyota Uhura", "attendant", 15),
        CrewMember("Jadzia Dax", "attendant", 12),
    ]

    # Flight Ops
    flight_ops = [
        CrewMember("Scotty", "flight_ops", 30),
        CrewMember("Geordi La Forge", "flight_ops", 15),
        CrewMember("Montgomery Scott", "flight_ops", 35),
        CrewMember("B'Elanna Torres", "flight_ops", 10),
        CrewMember("Reginald Barclay", "flight_ops", 8),
    ]

    p("Crew roster initialized.")

    # ------------------------------------------------------------------
    # CREATE SPACECRAFT OBJECTS
    # ------------------------------------------------------------------
    p("\n--- INITIALIZING SPACECRAFT FLEET ---")

    spacecraft_fleet = [
        Spacecraft("The Panic Capsule", seats=2, fuel_capacity=1000),
        Spacecraft("Event Horizon", seats=5, fuel_capacity=2500),
        Spacecraft("Serenity", seats=8, fuel_capacity=4000),
        Spacecraft("Millennium Falcon", seats=10, fuel_capacity=5000),
        Spacecraft("Nostromo", seats=25, fuel_capacity=10000),
    ]

    # ------------------------------------------------------------------
    # REFUEL FROM SHARED DEPOT
    # ------------------------------------------------------------------
    p("\n--- REFUELING FLEET ---")

    remaining_fuel = TOTAL_FUEL_POOL
    p(f"Total fuel available in depot: {remaining_fuel} units")

    for idx, craft in enumerate(spacecraft_fleet, start=1):
        if remaining_fuel <= 0:
            p("\n[NOTICE] Fuel depot is empty. No more fuel can be assigned.")
            break

        p(f"\nSpacecraft #{idx}: {craft.name}")
        p(f"  Fuel capacity: {craft.fuel_capacity} units")
        p(f"  Fuel currently on board: {craft.current_fuel} units")
        p(f"  Fuel remaining in depot: {remaining_fuel} units")

        max_for_this_ship = min(
            craft.fuel_capacity - craft.current_fuel,
            remaining_fuel,
        )
        if max_for_this_ship <= 0:
            p("  [INFO] This ship cannot take any more fuel.")
            continue

        amount = ask_int(
            f"  Enter fuel to load into {craft.name} (0-{max_for_this_ship})",
            min_value=0,
            max_value=max_for_this_ship,
        )

        craft.refuel(amount)
        remaining_fuel -= amount
        p(f"  [DEPOT] Fuel remaining in depot: {remaining_fuel} units")

    p("\n[SUMMARY] Fuel left in depot after initial allocation: {remaining_fuel} units")

    # ------------------------------------------------------------------
    # OPTIONAL FUEL RE-BALANCING PHASE
    # ------------------------------------------------------------------
    if ask_yes_no("Would you like to review and re-balance fuel allocations before mission planning?"):
        while True:
            p("\n--- FUEL REVIEW & RE-BALANCE ---")
            for idx, craft in enumerate(spacecraft_fleet, start=1):
                p(f"{idx}. {craft.name}: {craft.current_fuel}/{craft.fuel_capacity} units")
            p(f"Depot fuel remaining: {remaining_fuel} units")
            p("\nOptions:")
            p("  1) Move fuel from a ship back to the depot")
            p("  2) Add fuel from the depot to a ship")
            p("  3) Done re-balancing")
            choice = input("Select an option (1-3): ").strip()

            if choice == "1":
                ship_index = ask_int(
                    "  Select ship number to remove fuel from",
                    min_value=1,
                    max_value=len(spacecraft_fleet),
                )
                craft = spacecraft_fleet[ship_index - 1]
                if craft.current_fuel <= 0:
                    p("  [INFO] That ship has no fuel to remove.")
                    continue
                max_remove = craft.current_fuel
                amount = ask_int(
                    f"  Enter fuel to remove from {craft.name} (0-{max_remove})",
                    min_value=0,
                    max_value=max_remove,
                )
                removed = craft.remove_fuel(amount)
                remaining_fuel += removed
                p(f"  [DEPOT] Fuel remaining in depot: {remaining_fuel} units")

            elif choice == "2":
                if remaining_fuel <= 0:
                    p("  [INFO] The depot has no remaining fuel to allocate.")
                    continue
                ship_index = ask_int(
                    "  Select ship number to add fuel to",
                    min_value=1,
                    max_value=len(spacecraft_fleet),
                )
                craft = spacecraft_fleet[ship_index - 1]
                max_add = min(
                    craft.fuel_capacity - craft.current_fuel,
                    remaining_fuel,
                )
                if max_add <= 0:
                    p("  [INFO] That ship cannot take any more fuel.")
                    continue
                amount = ask_int(
                    f"  Enter fuel to add to {craft.name} (0-{max_add})",
                    min_value=0,
                    max_value=max_add,
                )
                craft.refuel(amount)
                remaining_fuel -= amount
                p(f"  [DEPOT] Fuel remaining in depot: {remaining_fuel} units")

            elif choice == "3":
                p("\n[SUMMARY] Final depot fuel after re-balance: {remaining_fuel} units")
                break
            else:
                p("  Please enter 1, 2, or 3.")

    # ------------------------------------------------------------------
    # CREW ASSIGNMENT
    # ------------------------------------------------------------------
    p("\n--- ASSIGNING CREW TO SPACECRAFT (INTERACTIVE) ---")
    for spacecraft in spacecraft_fleet:
        p("\nNow assigning crew for", spacecraft.name)
        assign_crew_interactively(
            spacecraft,
            captains,
            copilots,
            attendants,
            flight_ops,
        )

    # Status + rosters
    p("\n--- FINAL SPACECRAFT STATUS ---")
    for craft in spacecraft_fleet:
        p(craft.get_status())
        craft.print_crew_roster()

    # Readiness check
    p("\n--- CHECKING FLEET READINESS ---")
    for craft in spacecraft_fleet:
        craft.check_ready()

    # ------------------------------------------------------------------
    # MISSIONS
    # ------------------------------------------------------------------
    p("\n--- LOADING MISSIONS ---")
    missions = [
        Mission("Edge-of-Space Thrill Ride", "Low Earth Orbit", fuel_required=500),
        Mission("Aurora Orbit Experience", "Polar Orbit", fuel_required=1200),
        Mission("Lunar Flyby Adventure", "The Moon", fuel_required=3500),
    ]

    for mission in missions:
        mission.print_summary()

    # ------------------------------------------------------------------
    # MISSION PLANNING (ASSIGN SPACECRAFT)
    # ------------------------------------------------------------------
    p("\n" + "=" * 60)
    p("       MISSION PLANNING PHASE")
    p("=" * 60)

    available_spacecraft = list(spacecraft_fleet)
    for mission in missions:
        p("\nAssign a spacecraft to mission:", mission.name)
        choice = choose_from_list(available_spacecraft, "Available spacecraft:")
        if choice is None:
            p("  Skipping assignment for this mission.")
            continue

        if choice.can_handle_mission(mission):
            mission.assign_spacecraft(choice)
            available_spacecraft.remove(choice)
        else:
            p("  [ERROR] Selected spacecraft cannot handle this mission's fuel needs.")

    # ------------------------------------------------------------------
    # FUEL VS MISSION REQUIREMENTS REPORT
    # ------------------------------------------------------------------
    p("\n" + "=" * 60)
    p("        FUEL VS MISSION REQUIREMENTS REPORT")
    p("=" * 60)

    total_ship_fuel = sum(craft.current_fuel for craft in spacecraft_fleet)
    total_depot_fuel = remaining_fuel
    total_available_fuel = total_ship_fuel + total_depot_fuel

    total_mission_fuel_required = sum(m.fuel_required for m in missions)
    total_assigned_mission_fuel = sum(
        m.fuel_required for m in missions if m.spacecraft is not None
    )

    p(f"Total fuel originally available: {TOTAL_FUEL_POOL} units")
    p(f"  Fuel currently on ships:      {total_ship_fuel} units")
    p(f"  Fuel remaining in depot:      {total_depot_fuel} units")
    p(f"  Overall fuel accounted for:   {total_available_fuel} units")
    p("")
    p(f"Total fuel required for ALL missions:     {total_mission_fuel_required} units")
    p(f"Fuel required for ASSIGNED missions only: {total_assigned_mission_fuel} units")

    if total_available_fuel >= total_mission_fuel_required:
        p("  [CHECK] You have enough total fuel to cover all missions.")
    else:
        shortfall = total_mission_fuel_required - total_available_fuel
        p(f"  [WARNING] You are short by {shortfall} units for all missions combined.")

    if total_ship_fuel >= total_assigned_mission_fuel:
        p("  [CHECK] Ships collectively have enough fuel for assigned missions.")
    else:
        shortfall = total_assigned_mission_fuel - total_ship_fuel
        p(f"  [WARNING] Ships are short by {shortfall} units for assigned missions.")

    # ------------------------------------------------------------------
    # PASSENGER BOOKING (IF NOT QUICK MODE)
    # ------------------------------------------------------------------
    if not quick:
        p("\n--- PASSENGER BOOKING SIMULATION ---")
        sample_passengers = [
            "Alex", "Blake", "Casey", "Devon", "Emery",
            "Frankie", "Gale", "Harper", "Indigo", "Jordan",
        ]
        for mission in missions:
            if mission.spacecraft is None:
                continue
            p("\nBooking passengers for", mission.name)
            max_to_book = mission.spacecraft.seats
            for passenger in sample_passengers[:max_to_book]:
                if not mission.add_passenger(passenger):
                    break

    # Final readiness check
    p("\n--- FINAL MISSION READINESS CHECK ---")
    for mission in missions:
        p("\n" + "=" * 60)
        p("Checking", mission.name + "...")
        mission.mark_ready()

    # ------------------------------------------------------------------
    # LAUNCH SEQUENCE (IF NOT QUICK)
    # ------------------------------------------------------------------
    if not quick:
        p("\n" + "=" * 60)
        p("       LAUNCH SEQUENCE")
        p("=" * 60)

        for mission in missions:
            if mission.status == "ready":
                if ask_yes_no(f"Launch mission '{mission.name}' now?"):
                    result = mission.launch()
                    p(result)
                else:
                    p("[HOLD]", mission.name, "launch postponed.")
            else:
                p("[SKIP]", mission.name, "is not ready to launch.")

    # Wrap up
    p("\n" + "=" * 60)
    p("       END OF SIMULATION RUN")
    p("=" * 60)
    p("")
