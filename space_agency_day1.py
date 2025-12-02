# ============================================
# Stratos-FEAR Rides - Space Tourism Agency
# Day 1 Python Project
# ============================================

# --- Core Data: Variables ---
agency_name = "Stratos-FEAR Rides"
mission_focus = "Affordable Adrenaline-Forward Space Sightseeing"

# --- Lists: Things that can change ---
# Our astronaut pilots
astronauts = ["Jason", "Anthony", "Joshua", "Jeed", "James"]

# Our spacecraft fleet (name, seats per craft)
spacecraft_names = ["ThunderBolt", "StarScreamer", "EdgeRunner", "VoidDancer", "AuroraChaser"]
seats_per_spacecraft = [4, 4, 6, 4, 6]

# Available missions/destinations
missions = ["Edge-of-Space Thrill Ride", "Aurora Orbit Experience", "Lunar Flyby Adventure"]

# --- Tuples: Fixed data that won't change ---
# Fuel units needed for each mission type
fuel_requirements = (500, 1200, 3500)  # Edge-of-Space, Aurora Orbit, Lunar Flyby

# --- Simple Calculations ---
total_astronauts = len(astronauts)
total_spacecraft = len(spacecraft_names)
total_seats = sum(seats_per_spacecraft)

# Calculate fuel for first mission (Edge-of-Space)
first_mission_fuel = fuel_requirements[0]

# --- Print Summary ---
print("=" * 50)
print("SPACE AGENCY SUMMARY")
print("=" * 50)

print("Agency Name:", agency_name)
print("Mission Focus:", mission_focus)
print()

print("--- CREW ---")
print("Total Astronauts:", total_astronauts)
print("Astronaut Names:", astronauts)
print()

print("--- FLEET ---")
print("Total Spacecraft:", total_spacecraft)
print("Spacecraft Names:", spacecraft_names)
print("Total Passenger Seats Available:", total_seats)
print()

print("--- MISSIONS ---")
print("Available Missions:", missions)
print()

print("--- FIRST MISSION DETAILS ---")
print("Mission:", missions[0])
print("Estimated Fuel Units Needed:", first_mission_fuel)
print()

print("=" * 50)
print("Stratos-FEAR Rides: Feel the edge of space!")
print("=" * 50)
