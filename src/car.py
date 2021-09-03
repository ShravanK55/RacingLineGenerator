"""
Module for cars.
"""


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
