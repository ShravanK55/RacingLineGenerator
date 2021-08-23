"""
Module for cars.
"""


class Car:
    """
    Class representing a racing car.
    """
    
    def __init__(self, friction=1.6, mass=740.0, drag_coefficient=1.0, frontal_area=1.5):
        """
        Method to initialize a racing car. The defaults are set to the reference of an F1 car.
        
        Args:
            friction(float): Tyre friction co-efficient of the car. Defaults to 1.6.
                Default Reference: https://www.f1technical.net/forum/viewtopic.php?t=20627
            mass(float): Mass of the car in kg (including the driver). Defaults to 740.0 kg.
                Default Reference: https://en.wikipedia.org/wiki/Formula_One_car
            drag_coefficient(float): Drag co-efficient of the car. Defaults to 1.0.
                Default Reference: https://en.wikipedia.org/wiki/Automobile_drag_coefficient
            frontal_area(float): Frontal area of the car in m^2. Defaults to 1.5 m^2.
                Default Reference: https://www.f1technical.net/forum/viewtopic.php?t=11916

        """
        self.friction = friction
        self.mass = mass
        self.drag_coefficient = drag_coefficient
        self.frontal_area = frontal_area
