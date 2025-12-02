# ============================================
# Stratos-FEAR Rides - Space Tourism Agency
# Day 1 Python Project
# ============================================

# --- Core Data: Variables ---
agency_name = "Stratos-FEAR Rides"
mission_focus = "Affordable Adrenaline-Forward Space Sightseeing"
mission_statement = "At Stratos-FEAR Rides, our mission is to turn the thrill of space exploration into heart-pounding, unforgettable adventures. We bring the excitement of the cosmos closer than ever—one fearless ride at a time."

# --- Lists: Things that can change ---
# Our astronaut pilots (the student team)
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
print("Mission Statement:")
print(mission_statement)
print()

print("--- STUDENT TEAM ---")
print("Team Members:", astronauts)
print()

print("--- CREW ---")
print("Captains:", captains)
print("NPC Copilots:", npc_copilots)
print("Flight Attendants:", flight_attendants)
print("Flight Ops Crew:", flight_ops_crew)
print()

print("--- FLEET ---")
print("Total Spacecraft:", total_spacecraft)
print("Spacecraft Names:", spacecraft_names)
print("Total Passenger Seats Available:", total_seats)
print()

print("--- MISSIONS ---")
print("Available Missions:", missions)
print()

print("--- DESTINATIONS ---")
print("Available Destinations:", destinations)
print()

print("--- FIRST MISSION DETAILS ---")
print("Mission:", missions[0])
print("Estimated Fuel Units Needed:", first_mission_fuel)
print()

print("=" * 50)
print("Stratos-FEAR Rides: Feel the edge of space!")
print("=" * 50)
