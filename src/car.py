"""
Module for cars.
"""


class Car:
    """
    Class representing a racing car.
    """
    
    def __init__(self, friction=1.0):
        """
        Method to initialize a racing car.
        
        Args:
            friction(float): Tyre friction co-efficient of the car. Defaults to 1.0.

        """
        self.friction = friction
