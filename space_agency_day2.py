# ============================================
# Stratos-FEAR Rides - Space Tourism Agency
# Day 2 Python Project - Functions & Loops
# ============================================

# --- Core Data from Day 1 ---
agency_name = "Stratos-FEAR Rides"
mission_focus = "Affordable Adrenaline-Forward Space Sightseeing"
mission_statement = "At Stratos-FEAR Rides, our mission is to turn the thrill of space exploration into heart-pounding, unforgettable adventures. We bring the excitement of the cosmos closer than ever—one fearless ride at a time."

# Our student team
astronauts = ["Jason", "Anthony", "Joshua", "Jeed", "James"]

# Our spacecraft fleet (name, seats per craft)
spacecraft_names = ["The Panic Capsule", "The Black Pearl", "Serenity", "Millennium Falcon", "Heart of Gold"]
seats_per_spacecraft = [2, 5, 8, 10, 25]

# Crew members
captains = ["Zaphod Beeblebrox", "Han Solo", "Malcolm Reynolds", "Jean-Luc Picard", "Ellen Ripley"]
npc_copilots = ["Data", "TARS", "K-2SO", "Marvin the Paranoid Android", "C-3PO"]
flight_attendants = ["Trillian", "Leela", "Kaylee Frye", "Nyota Uhura", "Jadzia Dax"]
flight_ops_crew = ["Scotty", "Geordi La Forge", "Montgomery Scott", "B'Elanna Torres", "Reginald Barclay"]

# Available destinations
destinations = ["Mars", "Vulcan", "Pandora", "Arrakis", "Cybertron"]

# Available missions
missions = ["Edge-of-Space Thrill Ride", "Aurora Orbit Experience", "Lunar Flyby Adventure"]

# Fuel units needed for each mission type
fuel_requirements = (500, 1200, 3500)  # Edge-of-Space, Aurora Orbit, Lunar Flyby


# ============================================
# DAY 2: FUNCTIONS
# ============================================

def calculate_fuel(mission_index):
    """Calculate fuel needed for a specific mission."""
    fuel = fuel_requirements[mission_index]
    return fuel


def get_spacecraft_capacity(spacecraft_index):
    """Get the seat capacity for a specific spacecraft."""
    name = spacecraft_names[spacecraft_index]
    seats = seats_per_spacecraft[spacecraft_index]
    return name, seats


def print_mission_report(mission_name, fuel_needed):
    """Print a formatted report for a single mission."""
    print("  Mission:", mission_name)
    print("  Fuel Required:", fuel_needed, "units")
    print()


def find_available_spacecraft(group_size):
    """Find all spacecraft that can fit a customer group."""
    available = []
    for i in range(len(spacecraft_names)):
        if seats_per_spacecraft[i] >= group_size:
            available.append(spacecraft_names[i])
    return available


def get_crew_for_spacecraft(spacecraft_index):
    """Get the assigned crew for a specific spacecraft."""
    captain = captains[spacecraft_index]
    copilot = npc_copilots[spacecraft_index]
    attendant = flight_attendants[spacecraft_index]
    ops = flight_ops_crew[spacecraft_index]
    return captain, copilot, attendant, ops


# ============================================
# DAY 2: LOOPS AND REPORTS
# ============================================

# Print header
print("=" * 50)
print("STRATOS-FEAR RIDES - DAILY OPERATIONS REPORT")
print("=" * 50)
print("Agency:", agency_name)
print()
print("Mission Statement:")
print(mission_statement)
print()

# --- Loop through student team ---
print("--- STUDENT TEAM ---")
for student in astronauts:
    print("  Team Member:", student)
print()

# --- Loop through spacecraft and show crew assignments ---
print("--- FLEET & CREW ASSIGNMENTS ---")
total_capacity = 0
for i in range(len(spacecraft_names)):
    name, seats = get_spacecraft_capacity(i)
    captain, copilot, attendant, ops = get_crew_for_spacecraft(i)
    print("  " + name + " (" + str(seats) + " seats)")
    print("    Captain:", captain)
    print("    Copilot:", copilot)
    print("    Flight Attendant:", attendant)
    print("    Flight Ops:", ops)
    print()
    total_capacity = total_capacity + seats
print("Total Fleet Capacity:", total_capacity, "passengers")
print()

# --- Loop through destinations ---
print("--- AVAILABLE DESTINATIONS ---")
for destination in destinations:
    print("  -", destination)
print()

# --- Loop through missions and show fuel requirements ---
print("--- MISSION FUEL REPORT ---")
total_fuel = 0
for i in range(len(missions)):
    fuel = calculate_fuel(i)
    print_mission_report(missions[i], fuel)
    total_fuel = total_fuel + fuel

print("Total Fuel for All Missions:", total_fuel, "units")
print()

# --- Interactive Booking Feature ---
print("=" * 50)
print("CUSTOMER BOOKING SYSTEM")
print("=" * 50)

customer_group_sizes = input("Enter the number of people in your group (max 25): ")

if not customer_group_sizes.isdigit() or int(customer_group_sizes) < 1 or int(customer_group_sizes) > 25:
    print("We cannot accommodate that many people on one spacecraft.")
    print("Please enter a number between 1 and 25.")
else:
    customer_group_sizes = int(customer_group_sizes)
    available_spacecraft = find_available_spacecraft(customer_group_sizes)

    if len(available_spacecraft) == 0:
        print("Sorry, we don't have a spacecraft that can accommodate your group size.")
    else:
        print()
        print("Available spacecraft for your group of", customer_group_sizes, ":")
        for craft in available_spacecraft:
            print("  -", craft)

print()
print("=" * 50)
print("Stratos-FEAR Rides: Feel the edge of space!")
print("=" * 50)
