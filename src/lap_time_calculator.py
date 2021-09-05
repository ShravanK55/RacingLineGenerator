"""
Module to calculate lap times for a given car and racing line.
"""

from matplotlib import pyplot

from constants import AIR_DENSITY, GRAV_ACCELERATION


class LapTimeCalculator:
    """
    Class to calculate lap times for a given car and racing line.
    """

    def __init__(self):
        """
        Method to initialize the lap time calculator.
        """
        pass

    def calculate_lap_time(self, racing_line, car, starting_velocity=0.0, draw_graph=True):
        """
        Method to calculate the lap time of a car moving along a racing line.
        Calculation reference: http://www.jameshakewill.com/Lap_Time_Simulation.pdf (Pages 15 and 18)

        Args:
            racing_line(RacingLine): Racing line for the car to drive around.
            car(Car): Car that will drive on the racing line.
            starting_velocity(float): Velocity at which the car starts on the racing line in m/s. Defaults to 0.0.
            draw_graph(bool): Whether to plot the graph of exit velocity v/s sector time. Defaults to True.

        Returns:
            lap_time(float): Lap time taken by the car to drive around the racing line in seconds.

        """
        sectors = racing_line.sectors
        entry_velocity = starting_velocity
        entry_velocities = []
        exit_velocities = []

        # First pass to find the exit velocities of each sector (to apply acceleration/deceleration).
        for sector in sectors:
            exit_velocity = self.get_sector_exit_velocity(sector, car, entry_velocity)
            max_sector_velocity = self.get_sector_max_velocity(sector, car)
            entry_velocity = max_sector_velocity if entry_velocity > max_sector_velocity else entry_velocity
            exit_velocity = max_sector_velocity if exit_velocity > max_sector_velocity else exit_velocity
            entry_velocities.append(entry_velocity)
            exit_velocities.append(exit_velocity)
            entry_velocity = exit_velocity

        # Second pass to adjust the entry velocities of each sector based on the exit velocities (to apply braking).
        last_sector_idx = 0
        for current_sector_idx in reversed(range(len(sectors))):
            if (exit_velocities[current_sector_idx] > entry_velocities[last_sector_idx]):
                max_entry_velocity = self.get_sector_entry_velocity(
                    sectors[current_sector_idx], car, entry_velocities[last_sector_idx])
                if entry_velocities[current_sector_idx] > max_entry_velocity:
                    entry_velocities[current_sector_idx] = max_entry_velocity
                exit_velocities[current_sector_idx] = entry_velocities[last_sector_idx]

            last_sector_idx = current_sector_idx

        # Calculate the time taken for each sector.
        sector_times = []
        for idx in range(len(sectors)):
            sector_time = 2 * sectors[idx].length / (entry_velocities[idx] + exit_velocities[idx])
            sector_times.append(sector_time)

        dist_sum = 0
        distances = []
        for sector in sectors:
            dist_sum = dist_sum + sector.length
            distances.append(dist_sum)

        # Plotting a graph of the track distance v/s the velocity at that point.
        if draw_graph:
            pyplot.clf()
            pyplot.plot(distances, exit_velocities, label="Line")
            pyplot.xlabel("Distance (m)")
            pyplot.ylabel("Exit Velocity (m/s)")
            pyplot.title("Velocity Graph")
            pyplot.legend()
            pyplot.savefig("velocity_graph.png")

        # Calculating the lap time from the sector times.
        lap_time = 0.0
        for sector_time in sector_times:
            lap_time = lap_time + sector_time

        return lap_time

    def get_sector_max_velocity(self, sector, car):
        """
        Gets the maximum velocity a car can take around a sector.
        Reference: http://www.jameshakewill.com/Lap_Time_Simulation.pdf (Page 10)

        Args:
            sector(Sector): Reference to the sector that the car is travelling on.
            car(Car): Car that is moving through the sector.

        Returns:
            velocity(float): The maximum velocity a car can go while travelling in a sector in m/s.

        """
        total_force = car.friction * car.mass * GRAV_ACCELERATION
        drag = car.drag_coefficient * 0.5 * AIR_DENSITY * car.frontal_area
        denom = ((car.mass / sector.radius) ** 2) + (drag ** 2)
        denom = denom ** (1.0 / 4.0)
        velocity = (total_force ** (1.0 / 2.0)) / denom
        velocity = car.max_velocity if velocity > car.max_velocity else velocity
        return velocity

    def get_sector_entry_velocity(self, sector, car, exit_velocity):
        """
        Gets the entry velocity of a car through a sector from an exit velocity through braking.
        Reference: http://www.jameshakewill.com/Lap_Time_Simulation.pdf (Page 17)

        Args:
            sector(Sector): Reference to the sector that the car is travelling on.
            car(Car): Car that is moving through the sector.
            exit_velocity(float): Velocity with which the car exits the sector in m/s.

        Returns:
            entry_velocity(float): The maximum entry velocity of a car going into a given sector in m/s.

        """
        total_force = car.friction * car.mass * GRAV_ACCELERATION
        centripetal_force = car.mass * (exit_velocity ** 2) / sector.radius
        braking_force = ((total_force ** 2) - (centripetal_force ** 2)) ** (1.0 / 2.0)
        drag_force = car.drag_coefficient * 0.5 * AIR_DENSITY * (exit_velocity ** 2) * car.frontal_area
        decelerative_force = braking_force + drag_force
        delta_velocity = 2 * sector.length * decelerative_force / car.mass
        entry_velocity = ((exit_velocity ** 2) + delta_velocity) ** (1.0 / 2.0)
        entry_velocity = car.max_velocity if entry_velocity > car.max_velocity else entry_velocity
        return entry_velocity

    def get_sector_exit_velocity(self, sector, car, entry_velocity):
        """
        Gets the exit velocity of a car through a sector from an entry velocity through acceleration.
        Reference: http://www.jameshakewill.com/Lap_Time_Simulation.pdf (Page 10)

        Args:
            sector(Sector): Reference to the sector that the car is travelling on.
            car(Car): Car that is moving through the sector.
            entry_velocity(float): Velocity with which the car enters the sector in m/s.

        Returns:
            exit_velocity(float): The maximum exit velocity of a car going out a given sector in m/s.

        """
        drag_force = car.drag_coefficient * 0.5 * AIR_DENSITY * (entry_velocity ** 2) * car.frontal_area
        power = car.get_engine_power(entry_velocity)
        p_velocity = 1.0 if entry_velocity == 0.0 else entry_velocity
        acceleration = ((power / p_velocity) - drag_force) / car.mass
        max_acceleration = car.get_max_acceleration(entry_velocity)
        acceleration = max_acceleration if acceleration > max_acceleration else acceleration
        exit_velocity = ((entry_velocity ** 2) + (2 * acceleration * sector.length)) ** (1.0 / 2.0)
        exit_velocity = car.max_velocity if exit_velocity > car.max_velocity else exit_velocity
        return exit_velocity

