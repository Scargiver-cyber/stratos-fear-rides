# stratosfear/classes.py
# Core game entities: CrewMember, Spacecraft, Mission

from .utils import p


class CrewMember:
    """Represents a crew member (captain, copilot, attendant, or flight ops)."""

    def __init__(self, name, role, experience=0):
        self.name = name
        self.role = role
        # Simple numeric rating used to represent crew skill / time in service.
        # Higher values will positively influence readiness checks.
        self.experience = experience
        self.assigned_spacecraft = None

    def assign_to_spacecraft(self, spacecraft):
        """Assign this crew member to a spacecraft."""
        if self.assigned_spacecraft is not None:
            p("  [WARN]", self.name,
              "is already assigned to", self.assigned_spacecraft.name)
            return False
        self.assigned_spacecraft = spacecraft
        p("  [CREW]", self.name, "assigned as", self.role, "to", spacecraft.name)
        return True

    def __str__(self):
        assigned = (
            self.assigned_spacecraft.name if self.assigned_spacecraft else "Unassigned"
        )
        return f"{self.name} ({self.role}, XP {self.experience}, {assigned})"


class Spacecraft:
    """Represents a spacecraft in the Stratos-FEAR fleet."""

    def __init__(self, name, seats, fuel_capacity):
        self.name = name
        self.seats = seats
        self.fuel_capacity = fuel_capacity
        self.current_fuel = 0
        self.ready = False
        self.crew = {
            "captain": None,
            "copilot": None,
            "attendant": None,
            "flight_ops": None,
        }

    def __str__(self):
        fuel_pct = int(
            (self.current_fuel / self.fuel_capacity) * 100
        ) if self.fuel_capacity else 0
        return f"{self.name} | Seats: {self.seats} | Fuel: {fuel_pct}%"

    def refuel(self, amount):
        """Add fuel to the spacecraft (up to capacity)."""
        self.current_fuel = min(self.current_fuel + amount, self.fuel_capacity)
        p("  [FUEL]", self.name, "refueled to",
          self.current_fuel, "/", self.fuel_capacity, "units")
        return self.current_fuel

    def remove_fuel(self, amount):
        """Remove fuel from the spacecraft, returning it to the depot."""
        if amount <= 0:
            return 0
        removed = min(self.current_fuel, amount)
        self.current_fuel -= removed
        p("  [FUEL]", self.name, "had", removed,
          "units removed; now", self.current_fuel, "/", self.fuel_capacity, "units")
        return removed

    def assign_crew_member(self, crew_member):
        """Assign a crew member to their role on this spacecraft."""
        role = crew_member.role
        if role not in self.crew:
            p("  [ERROR] Unknown role:", role)
            return False
        if self.crew[role] is not None:
            p("  [ERROR]", self.name, "already has a", role)
            return False
        if crew_member.assign_to_spacecraft(self):
            self.crew[role] = crew_member
            return True
        return False


    def unassign_crew_member(self, role):
        """Remove a crew member from this spacecraft by role and return the member.

        This is used to support interactive reassignment between ships.
        """
        if role not in self.crew:
            p("  [ERROR]", self.name, "has no crew slot for role:", role)
            return None
        member = self.crew[role]
        if member is None:
            p("  [INFO]", self.name, "has no", role, "assigned to remove.")
            return None
        # Detach the crew member from this spacecraft
        member.assigned_spacecraft = None
        self.crew[role] = None
        p("  [CREW]", member.name, "removed from", self.name, "as", role)
        return member

    def get_crew_experience_score(self):
        """Return the total experience score of all assigned crew."""
        return sum(
            (member.experience for member in self.crew.values() if member is not None),
            0,
        )

    def check_ready(self):
        """Check if spacecraft is ready for launch (fuel + crew + experience)."""
        if self.fuel_capacity:
            fuel_ratio = self.current_fuel / self.fuel_capacity
        else:
            fuel_ratio = 0.0

        exp_score = self.get_crew_experience_score()

        # Highly experienced crews can safely launch with slightly less fuel buffer.
        # Rookie crews must meet the full 50% fuel threshold.
        if exp_score >= 60:
            required_fuel_ratio = 0.40
            exp_label = "ELITE CREW"
        elif exp_score >= 30:
            required_fuel_ratio = 0.45
            exp_label = "VETERAN CREW"
        else:
            required_fuel_ratio = 0.50
            exp_label = "ROOKIE CREW"

        has_fuel = fuel_ratio >= required_fuel_ratio
        has_captain = self.crew["captain"] is not None

        p(
            f"  [CREW XP] {self.name} experience score: {exp_score} "
            f"({exp_label}, fuel threshold {int(required_fuel_ratio * 100)}%)"
        )

        if has_fuel and has_captain:
            self.ready = True
            p("  [READY]", self.name, "is prepped for launch!")
            return True

        reasons = []
        if not has_fuel:
            reasons.append("needs more fuel")
        if not has_captain:
            reasons.append("needs a captain")
        p("  [NOT READY]", self.name + ":", ", ".join(reasons))
        return False

    def can_handle_mission(self, mission):
        """Check if this spacecraft can handle a given mission (fuel check only)."""
        has_fuel = self.current_fuel >= mission.fuel_required
        if has_fuel:
            p("  [OK]", self.name, "can handle", mission.name)
            return True
        p("  [NOPE]", self.name, "does NOT have enough fuel for", mission.name)
        return False

    def get_status(self):
        """Return a status string for this spacecraft."""
        ready_status = "Ready" if self.ready else "Not Ready"
        fuel_pct = int((self.current_fuel / self.fuel_capacity) * 100) if self.fuel_capacity else 0
        crew_count = sum(1 for c in self.crew.values() if c is not None)
        return (
            f"{self.name} | Seats: {self.seats}"
            f" | Fuel: {fuel_pct}% | Crew: {crew_count}/4 | {ready_status}"
        )

    def print_crew_roster(self):
        """Print a summary of the crew assigned to this spacecraft."""
        p("")
        p("Crew Roster for", self.name)
        p("-" * 40)
        for role, member in self.crew.items():
            if member:
                p(f"  {role.capitalize()}: {member.name} (XP {member.experience})")
            else:
                p(f"  {role.capitalize()}: [Unassigned]")


class Mission:
    """Represents a space tourism mission for Stratos-FEAR."""

    def __init__(self, name, destination, fuel_required):
        self.name = name
        self.destination = destination
        self.fuel_required = fuel_required
        self.spacecraft = None
        self.passengers = []
        self.status = "planning"

    def __str__(self):
        return f"{self.name} -> {self.destination} (Fuel required: {self.fuel_required})"

    def assign_spacecraft(self, spacecraft):
        """Assign a spacecraft to this mission."""
        self.spacecraft = spacecraft
        p("  [MISSION]", self.name, "assigned to", spacecraft.name)

    def add_passenger(self, passenger_name):
        """Add a passenger to the mission (if seats remain)."""
        if self.spacecraft is None:
            p("  [ERROR] Cannot add passenger, no spacecraft assigned")
            return False
        if len(self.passengers) >= self.spacecraft.seats:
            p("  [ERROR] Mission is full (",
              len(self.passengers), "/", self.spacecraft.seats, ")")
            return False
        self.passengers.append(passenger_name)
        p("  [BOOKED]", passenger_name, "added to", self.name)
        return True

    def mark_ready(self):
        """Check if mission can be marked ready."""
        if self.spacecraft is None:
            p("  [ERROR]", self.name, "has no spacecraft assigned")
            return False
        if not self.spacecraft.ready:
            p("  [ERROR]", self.spacecraft.name, "is not ready")
            return False
        if len(self.passengers) == 0:
            p("  [ERROR]", self.name, "has no passengers")
            return False

        # Report on crew experience for this mission when marking ready.
        exp_score = self.spacecraft.get_crew_experience_score()
        if exp_score >= 60:
            exp_label = "ELITE CREW"
        elif exp_score >= 30:
            exp_label = "VETERAN CREW"
        else:
            exp_label = "ROOKIE CREW"
        p(f"  [CREW XP] {self.name} is crewed by a {exp_label} (XP {exp_score}).")

        self.status = "ready"
        p("  [READY] Mission", self.name, "is GO FOR LAUNCH!")
        return True

    def launch(self):
        """Attempt to launch the mission."""
        if self.status != "ready":
            return (
                "[ABORT] " + self.name +
                " status is '" + self.status + "', not 'ready'"
            )
        self.status = "launched"
        captain = self.spacecraft.crew["captain"]
        exp_score = self.spacecraft.get_crew_experience_score()
        if exp_score >= 60:
            exp_flavor = "with a legendary, battle-tested crew"
        elif exp_score >= 30:
            exp_flavor = "with a seasoned veteran crew"
        else:
            exp_flavor = "with a green but eager crew"

        return (
            "[LAUNCH] " + self.name + "! "
            + self.spacecraft.name + " has lifted off under Captain "
            + (captain.name if captain else "Unknown")
            + " with " + str(len(self.passengers))
            + " passengers bound for " + self.destination + " "
            + exp_flavor + "!"
        )

    def print_summary(self):
        """Print a detailed mission summary."""
        p("")
        p("=" * 50)
        p("MISSION:", self.name)
        p("=" * 50)
        p("  Destination:", self.destination)
        p("  Fuel Required:", self.fuel_required, "units")
        p("  Status:", self.status.upper())
        if self.spacecraft:
            p("  Spacecraft:", self.spacecraft.name)
        else:
            p("  Spacecraft: Not assigned")
        if self.passengers:
            p("  Passengers:", len(self.passengers))
        else:
            p("  Passengers: None booked")
        p("=" * 50)
