"""
Module for cars.
"""

from constants import AIR_DENSITY, GRAV_ACCELERATION


class Car:
    """
    Class representing a racing car.
    Defaults values are set with respect to a modern Formula 1 car.
    """
    
    def __init__(self, max_velocity=100.0, max_acceleration=15.5, friction=1.6, mass=740.0, drag_coefficient=1.0,
                 frontal_area=1.5, base_engine_power=100000.0, max_engine_power=800000.0):
        """
        Method to initialize a racing car. The defaults are set to the reference of a modern Formula 1 car.
        
        Args:
            max_velocity(float): Maximum velocity of the car in m/s. Defaults to 100.0 m/s (360 kmph).
                Default Reference: https://en.wikipedia.org/wiki/Formula_One_car
            max_acceleration(float): Maximum acceleration of the car in m/s^2. Defaults to 15.5 m/s^2.
                Default Reference: https://en.wikipedia.org/wiki/Formula_One_car
            friction(float): Tyre friction co-efficient of the car. Defaults to 1.6.
                Default Reference: https://www.f1technical.net/forum/viewtopic.php?t=20627
            mass(float): Mass of the car in kg (including the driver). Defaults to 740.0 kg.
                Default Reference: https://en.wikipedia.org/wiki/Formula_One_car
            drag_coefficient(float): Drag co-efficient of the car. Defaults to 1.0.
                Default Reference: https://en.wikipedia.org/wiki/Automobile_drag_coefficient
            frontal_area(float): Frontal area of the car in m^2. Defaults to 1.5 m^2.
                Default Reference: https://www.f1technical.net/forum/viewtopic.php?t=11916
            base_engine_power(float): Base engine power of the car in watts. Defaults to 100000.0 W.
                Default Reference: https://en.wikipedia.org/wiki/Formula_One_engines
            max_engine_power(float): Maximum engine power of the car in watts. Defaults to 800000.0 W.
                Default Reference: https://en.wikipedia.org/wiki/Formula_One_car

        """
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        self.friction = friction
        self.mass = mass
        self.drag_coefficient = drag_coefficient
        self.frontal_area = frontal_area
        self.base_engine_power = base_engine_power
        self.max_engine_power = max_engine_power

    def get_engine_power(self, velocity):
        """
        Gets the engine power of a car at a particular velocity.

        Args:
            velocity(float): Velocity of the car in m/s.

        Returns:
            engine_power(float): Engine power of the car at the given velocity in watts.

        """
        diff = self.max_engine_power - self.base_engine_power
        engine_power = self.base_engine_power
        
        if velocity >= 0.0 and velocity < 10.0:
            engine_power = engine_power + (diff * 0.2)
        elif velocity >= 10.0 and velocity < 40.0:
            engine_power = engine_power + (diff * 0.5)
        elif velocity >= 40.0 and velocity < 70.0:
            engine_power = engine_power + (diff * 0.7)
        elif velocity >= 70.0 and velocity < 90.0:
            engine_power = engine_power + (diff * 0.9)
        else:
            engine_power = self.max_engine_power
        
        return engine_power

    def get_max_velocity(self, sector):
        """
        Gets the maximum velocity a car can take around a sector.
        Reference: http://www.jameshakewill.com/Lap_Time_Simulation.pdf (Page 10)
        
        Args:
            sector(Sector): Reference to the sector that the car is travelling on.
        
        Returns:
            velocity(float): The maximum velocity a car can go while travelling in a sector in m/s.

        """
        total_force = self.friction * self.mass * GRAV_ACCELERATION
        drag = self.drag_coefficient * 0.5 * AIR_DENSITY * self.frontal_area
        denom = ((self.mass / sector.radius) ** 2) + (drag ** 2)
        denom = denom ** (1.0 / 4.0)
        velocity = (total_force ** (1.0 / 2.0)) / denom
        velocity = self.max_velocity if velocity > self.max_velocity else velocity
        return velocity

    def get_max_acceleration(self, velocity):
        """
        Gets the maximum acceleration a car can have at a given velocity.
        Reference: https://en.wikipedia.org/wiki/Formula_One_car#Acceleration
        
        Args:
            velocity(float): Velocity that the car is currently running at.
        
        Returns:
            acceleration(float): The maximum velocity a car can go while travelling in a sector in m/s.

        """
        acceleration = self.max_acceleration
        
        # 0-100 kmph.
        if velocity >= 0.0 and velocity < 28.0:
            acceleration = acceleration * 0.75
        # 100-200 kmph.
        elif velocity >= 28.0 and velocity < 56.0:
            acceleration = acceleration * 1.0
        # 200-300 kmph.
        elif velocity >= 56.0 and velocity < 84.0:
            acceleration = acceleration * 0.45
        # 300 kmph - Max Speed.
        elif velocity >= 84.0 and velocity < self.max_velocity:
            acceleration = acceleration * 0.3
        else:
            acceleration = 0.0
        
        return acceleration

    def get_entry_velocity(self, sector, exit_velocity):
        """
        Gets the entry velocity of a car through a sector from an exit velocity through braking.
        Reference: http://www.jameshakewill.com/Lap_Time_Simulation.pdf (Page 17)
        
        Args:
            sector(Sector): Reference to the sector that the car is travelling on.
            exit_velocity(float): Velocity with which the car exits the sector in m/s.
        
        Returns:
            entry_velocity(float): The maximum entry velocity of a car going into a given sector in m/s.

        """
        total_force = self.friction * self.mass * GRAV_ACCELERATION
        centripetal_force = self.mass * (exit_velocity ** 2) / sector.radius
        braking_force = ((total_force ** 2) - (centripetal_force ** 2)) ** (1.0 / 2.0)
        drag_force = self.drag_coefficient * 0.5 * AIR_DENSITY * (exit_velocity ** 2) * self.frontal_area
        decelerative_force = braking_force + drag_force
        delta_velocity = 2 * sector.length * decelerative_force / self.mass
        entry_velocity = ((exit_velocity ** 2) + delta_velocity) ** (1.0 / 2.0)
        entry_velocity = self.max_velocity if entry_velocity > self.max_velocity else entry_velocity
        return entry_velocity

    def get_exit_velocity(self, sector, entry_velocity):
        """
        Gets the exit velocity of a car through a sector from an entry velocity through acceleration.
        Reference: http://www.jameshakewill.com/Lap_Time_Simulation.pdf (Page 10)
        
        Args:
            sector(Sector): Reference to the sector that the car is travelling on.
            entry_velocity(float): Velocity with which the car enters the sector in m/s.
        
        Returns:
            exit_velocity(float): The maximum exit velocity of a car going out a given sector in m/s.

        """
        drag_force = self.drag_coefficient * 0.5 * AIR_DENSITY * (entry_velocity ** 2) * self.frontal_area
        power = self.get_engine_power(entry_velocity)
        p_velocity = 1.0 if entry_velocity == 0.0 else entry_velocity
        acceleration = ((power / p_velocity) - drag_force) / self.mass
        max_acceleration = self.get_max_acceleration(entry_velocity)
        acceleration = max_acceleration if acceleration > max_acceleration else acceleration
        exit_velocity = ((entry_velocity ** 2) + (2 * acceleration * sector.length)) ** (1.0 / 2.0)
        exit_velocity = self.max_velocity if exit_velocity > self.max_velocity else exit_velocity
        return exit_velocity
