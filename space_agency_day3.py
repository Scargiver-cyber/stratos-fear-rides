# ============================================
# Stratos-FEAR Rides - Space Tourism Agency
# Day 3 Python Project - Classes & OOP
# ============================================

"""
Day 3 introduces Object-Oriented Programming with three core classes:
- CrewMember: Captains, copilots, attendants, and flight ops
- Spacecraft: Vehicles with capacity, fuel, and assigned crew
- Mission: Ties together spacecraft, crew, and destinations
"""


# =============================================================================
# CREWMEMBER CLASS
# =============================================================================

class CrewMember:
    """
    Represents a crew member for Stratos-FEAR spacecraft.

    Attributes:
        name (str): Crew member's name
        role (str): Job role - captain, copilot, attendant, or flight_ops
        experience_level (int): Years of experience (0-20)
        certified (bool): Whether crew member is flight-certified
        assigned_spacecraft (Spacecraft): Current spacecraft assignment
    """

    def __init__(self, name, role, experience_level=0):
        """Initialize a new crew member with name, role, and experience."""
        self.name = name
        self.role = role
        self.experience_level = experience_level
        self.certified = False
        self.assigned_spacecraft = None

    def certify(self):
        """Mark the crew member as flight-certified."""
        self.certified = True
        print("  [CERTIFIED]", self.name, "is now certified for flight!")

    def assign_to_spacecraft(self, spacecraft):
        """Attempt to assign crew member to a spacecraft."""
        if not self.certified:
            print("  [ERROR]", self.name, "cannot be assigned - not certified!")
            return False
        if self.assigned_spacecraft is not None:
            print("  [ERROR]", self.name, "already assigned to", self.assigned_spacecraft.name)
            return False
        self.assigned_spacecraft = spacecraft
        print("  [ASSIGNED]", self.name, "->", spacecraft.name)
        return True

    def get_status(self):
        """Return a status string for this crew member."""
        cert_status = "Certified" if self.certified else "Not Certified"
        if self.assigned_spacecraft:
            assignment = "Assigned to " + self.assigned_spacecraft.name
        else:
            assignment = "Available"
        return self.name + " (" + self.role + ") | " + cert_status + " | " + assignment


# =============================================================================
# SPACECRAFT CLASS
# =============================================================================

class Spacecraft:
    """
    Represents a spacecraft in the Stratos-FEAR fleet.

    Attributes:
        name (str): Spacecraft name
        seats (int): Passenger capacity
        fuel_capacity (int): Maximum fuel units
        current_fuel (int): Current fuel level
        ready (bool): Whether craft is ready for launch
        crew (dict): Assigned crew by role
    """

    def __init__(self, name, seats, fuel_capacity):
        """Initialize spacecraft with name, seats, and fuel capacity."""
        self.name = name
        self.seats = seats
        self.fuel_capacity = fuel_capacity
        self.current_fuel = 0
        self.ready = False
        self.crew = {
            "captain": None,
            "copilot": None,
            "attendant": None,
            "flight_ops": None
        }

    def refuel(self, amount):
        """Add fuel to the spacecraft (up to capacity)."""
        self.current_fuel = min(self.current_fuel + amount, self.fuel_capacity)
        print("  [FUEL]", self.name, "refueled to", self.current_fuel, "/", self.fuel_capacity, "units")
        return self.current_fuel

    def assign_crew_member(self, crew_member):
        """Assign a crew member to their role on this spacecraft."""
        role = crew_member.role
        if role not in self.crew:
            print("  [ERROR] Unknown role:", role)
            return False
        if self.crew[role] is not None:
            print("  [ERROR]", self.name, "already has a", role)
            return False
        if crew_member.assign_to_spacecraft(self):
            self.crew[role] = crew_member
            return True
        return False

    def check_ready(self):
        """Check if spacecraft is ready for launch (fuel + crew)."""
        # Need at least 50% fuel
        has_fuel = self.current_fuel >= self.fuel_capacity * 0.5
        # Need at least a captain
        has_captain = self.crew["captain"] is not None

        if has_fuel and has_captain:
            self.ready = True
            print("  [READY]", self.name, "is prepped for launch!")
            return True
        else:
            reasons = []
            if not has_fuel:
                reasons.append("needs more fuel")
            if not has_captain:
                reasons.append("needs a captain")
            print("  [NOT READY]", self.name + ":", ", ".join(reasons))
            return False

    def can_handle_mission(self, mission):
        """Check if this spacecraft can handle a given mission."""
        has_fuel = self.current_fuel >= mission.fuel_required
        if has_fuel:
            print("  [OK]", self.name, "can handle", mission.name)
            return True
        else:
            print("  [FAIL]", self.name, "needs", mission.fuel_required, "fuel, has", self.current_fuel)
            return False

    def get_status(self):
        """Return a status string for this spacecraft."""
        ready_status = "Ready" if self.ready else "Not Ready"
        fuel_pct = int((self.current_fuel / self.fuel_capacity) * 100)
        crew_count = sum(1 for c in self.crew.values() if c is not None)
        return self.name + " | Seats: " + str(self.seats) + " | Fuel: " + str(fuel_pct) + "% | Crew: " + str(crew_count) + "/4 | " + ready_status

    def print_crew_roster(self):
        """Print the crew roster for this spacecraft."""
        print("  Crew Roster for", self.name + ":")
        for role, member in self.crew.items():
            if member:
                print("    ", role.capitalize() + ":", member.name)
            else:
                print("    ", role.capitalize() + ": (vacant)")


# =============================================================================
# MISSION CLASS
# =============================================================================

class Mission:
    """
    Represents a space tourism mission for Stratos-FEAR.

    Attributes:
        name (str): Mission name
        destination (str): Where we're going
        fuel_required (int): Fuel units needed
        spacecraft (Spacecraft): Assigned spacecraft
        passengers (list): List of passenger names
        status (str): planning, ready, launched, or completed
    """

    def __init__(self, name, destination, fuel_required):
        """Initialize a new mission."""
        self.name = name
        self.destination = destination
        self.fuel_required = fuel_required
        self.spacecraft = None
        self.passengers = []
        self.status = "planning"

    def assign_spacecraft(self, spacecraft):
        """Assign a spacecraft to this mission."""
        if spacecraft.can_handle_mission(self):
            self.spacecraft = spacecraft
            print("  [ASSIGNED]", spacecraft.name, "to mission", self.name)
            return True
        return False

    def add_passenger(self, passenger_name):
        """Add a passenger to the mission."""
        if self.spacecraft is None:
            print("  [ERROR] No spacecraft assigned yet")
            return False
        if len(self.passengers) >= self.spacecraft.seats:
            print("  [ERROR] Mission is full (", len(self.passengers), "/", self.spacecraft.seats, ")")
            return False
        self.passengers.append(passenger_name)
        print("  [BOOKED]", passenger_name, "added to", self.name)
        return True

    def mark_ready(self):
        """Check if mission can be marked ready."""
        if self.spacecraft is None:
            print("  [ERROR]", self.name, "has no spacecraft assigned")
            return False
        if not self.spacecraft.ready:
            print("  [ERROR]", self.spacecraft.name, "is not ready")
            return False
        if len(self.passengers) == 0:
            print("  [ERROR]", self.name, "has no passengers")
            return False
        self.status = "ready"
        print("  [READY] Mission", self.name, "is GO FOR LAUNCH!")
        return True

    def launch(self):
        """Attempt to launch the mission."""
        if self.status != "ready":
            return "[ABORT] " + self.name + " status is '" + self.status + "', not 'ready'"
        self.status = "launched"
        captain = self.spacecraft.crew["captain"]
        return "[LAUNCH] " + self.name + "! " + self.spacecraft.name + " commanded by " + captain.name + " with " + str(len(self.passengers)) + " passengers bound for " + self.destination + "!"

    def print_summary(self):
        """Print a detailed mission summary."""
        print()
        print("=" * 50)
        print("MISSION:", self.name)
        print("=" * 50)
        print("  Destination:", self.destination)
        print("  Fuel Required:", self.fuel_required, "units")
        print("  Status:", self.status.upper())
        if self.spacecraft:
            print("  Spacecraft:", self.spacecraft.name)
        else:
            print("  Spacecraft: Not assigned")
        if self.passengers:
            print("  Passengers:", len(self.passengers))
            for p in self.passengers:
                print("    -", p)
        else:
            print("  Passengers: None booked")
        print("=" * 50)


# =============================================================================
# MAIN SIMULATION
# =============================================================================

if __name__ == "__main__":

    # Agency header
    print()
    print("=" * 60)
    print("       STRATOS-FEAR RIDES - MISSION CONTROL")
    print("       'Feel the edge of space!'")
    print("=" * 60)
    print()

    # -------------------------------------------------------------------------
    # CREATE CREW MEMBER OBJECTS
    # -------------------------------------------------------------------------
    print("--- INITIALIZING CREW ROSTER ---")

    # Captains
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

    # Certify all crew
    print()
    print("--- CERTIFYING ALL CREW ---")
    all_crew = captains + copilots + attendants + flight_ops
    for crew in all_crew:
        crew.certify()

    # -------------------------------------------------------------------------
    # CREATE SPACECRAFT OBJECTS
    # -------------------------------------------------------------------------
    print()
    print("--- INITIALIZING FLEET ---")
    spacecraft_fleet = [
        Spacecraft("The Panic Capsule", seats=2, fuel_capacity=1000),
        Spacecraft("The Black Pearl", seats=5, fuel_capacity=2500),
        Spacecraft("Serenity", seats=8, fuel_capacity=4000),
        Spacecraft("Millennium Falcon", seats=10, fuel_capacity=5000),
        Spacecraft("Heart of Gold", seats=25, fuel_capacity=10000),
    ]

    # Refuel all spacecraft
    print()
    print("--- REFUELING FLEET ---")
    for craft in spacecraft_fleet:
        craft.refuel(craft.fuel_capacity)  # Fill 'em up!

    # Assign crew to spacecraft (one crew set per ship)
    print()
    print("--- ASSIGNING CREW TO SPACECRAFT ---")
    for i, craft in enumerate(spacecraft_fleet):
        print()
        print("Crewing", craft.name + ":")
        craft.assign_crew_member(captains[i])
        craft.assign_crew_member(copilots[i])
        craft.assign_crew_member(attendants[i])
        craft.assign_crew_member(flight_ops[i])

    # Check readiness
    print()
    print("--- CHECKING FLEET READINESS ---")
    for craft in spacecraft_fleet:
        craft.check_ready()

    # -------------------------------------------------------------------------
    # CREATE MISSION OBJECTS
    # -------------------------------------------------------------------------
    print()
    print("--- LOADING MISSIONS ---")
    missions = [
        Mission("Edge-of-Space Thrill Ride", "Low Earth Orbit", fuel_required=500),
        Mission("Aurora Orbit Experience", "Polar Orbit", fuel_required=1200),
        Mission("Lunar Flyby Adventure", "The Moon", fuel_required=3500),
    ]

    # Print initial mission summaries
    for mission in missions:
        mission.print_summary()

    # -------------------------------------------------------------------------
    # MISSION PLANNING SIMULATION
    # -------------------------------------------------------------------------
    print()
    print("=" * 60)
    print("       MISSION PLANNING PHASE")
    print("=" * 60)

    # Assign spacecraft to missions
    print()
    print("--- ASSIGNING SPACECRAFT TO MISSIONS ---")
    missions[0].assign_spacecraft(spacecraft_fleet[0])  # Panic Capsule for Edge-of-Space
    missions[1].assign_spacecraft(spacecraft_fleet[2])  # Serenity for Aurora Orbit
    missions[2].assign_spacecraft(spacecraft_fleet[4])  # Heart of Gold for Lunar Flyby

    # Add passengers (student team as test passengers!)
    print()
    print("--- BOOKING PASSENGERS ---")
    student_team = ["Jason", "Anthony", "Joshua", "Jeed", "James"]

    print()
    print("Booking for", missions[0].name + ":")
    missions[0].add_passenger(student_team[0])  # Jason on Edge-of-Space
    missions[0].add_passenger(student_team[1])  # Anthony on Edge-of-Space

    print()
    print("Booking for", missions[1].name + ":")
    missions[1].add_passenger(student_team[2])  # Joshua on Aurora Orbit
    missions[1].add_passenger(student_team[3])  # Jeed on Aurora Orbit

    print()
    print("Booking for", missions[2].name + ":")
    missions[2].add_passenger(student_team[4])  # James on Lunar Flyby

    # -------------------------------------------------------------------------
    # LAUNCH READINESS CHECK
    # -------------------------------------------------------------------------
    print()
    print("=" * 60)
    print("       LAUNCH READINESS CHECK")
    print("=" * 60)
    print()

    for mission in missions:
        print("Checking", mission.name + "...")
        mission.mark_ready()

    # -------------------------------------------------------------------------
    # LAUNCH SEQUENCE
    # -------------------------------------------------------------------------
    print()
    print("=" * 60)
    print("       LAUNCH SEQUENCE")
    print("=" * 60)
    print()

    for mission in missions:
        result = mission.launch()
        print(result)

    # -------------------------------------------------------------------------
    # FINAL STATUS REPORT
    # -------------------------------------------------------------------------
    print()
    print("=" * 60)
    print("       FINAL STATUS REPORT")
    print("=" * 60)

    print()
    print("--- FLEET STATUS ---")
    for craft in spacecraft_fleet:
        print(" ", craft.get_status())
        craft.print_crew_roster()
        print()

    print("--- MISSION STATUS ---")
    for mission in missions:
        mission.print_summary()

    print()
    print("=" * 60)
    print("       END OF SIMULATION")
    print("       Stratos-FEAR Rides: Feel the edge of space!")
    print("=" * 60)
    print()
