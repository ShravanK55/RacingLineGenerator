"""
Module for cars.
"""

from constants import AIR_DENSITY, GRAV_ACCELERATION


class Car:
    """
    Class representing a racing car.
    """
    
    def __init__(self, max_velocity=100.0, friction=1.6, mass=740.0, drag_coefficient=1.0, frontal_area=1.5,
                 engine_power=810000.0):
        """
        Method to initialize a racing car. The defaults are set to the reference of an F1 car.
        
        Args:
            max_velocity(float): Maximum velocity of the car in m/s. Defaults to 100.0 m/s (360 kmph).
                Default Reference: https://en.wikipedia.org/wiki/Formula_One_car
            friction(float): Tyre friction co-efficient of the car. Defaults to 1.6.
                Default Reference: https://www.f1technical.net/forum/viewtopic.php?t=20627
            mass(float): Mass of the car in kg (including the driver). Defaults to 740.0 kg.
                Default Reference: https://en.wikipedia.org/wiki/Formula_One_car
            drag_coefficient(float): Drag co-efficient of the car. Defaults to 1.0.
                Default Reference: https://en.wikipedia.org/wiki/Automobile_drag_coefficient
            frontal_area(float): Frontal area of the car in m^2. Defaults to 1.5 m^2.
                Default Reference: https://www.f1technical.net/forum/viewtopic.php?t=11916
            engine_power(float): Engine power of the car in watts. Defaults to 810000.0 W.
                Default Reference: https://en.wikipedia.org/wiki/Formula_One_car

        """
        self.max_velocity = max_velocity
        self.friction = friction
        self.mass = mass
        self.drag_coefficient = drag_coefficient
        self.frontal_area = frontal_area
        self.engine_power = engine_power
    
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
