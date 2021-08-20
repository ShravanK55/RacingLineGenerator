"""
Module for racing lines.
"""

import math

class RacingLine:
    """
    Class representing a racing line.
    """
    
    def __init__(self, vertices=None):
        """
        Method to initialize a racing line.
        
        Args:
            vertices(list): List of vertices present in the racing line. Defaults to None.

        """
        self.vertices = []
        if vertices is not None:
            self.vertices = vertices
            
    @property
    def distance(self):
        """
        Gets the distance of a racing line.
        """
        if not self.vertices:
            return 0
        
        distance = 0
        prev_vert = self.vertices[0]
        
        for vertex in self.vertices:
            distance = distance + math.sqrt(((vertex.x - prev_vert.x) ** 2) +
                                            ((vertex.y - prev_vert.y) ** 2) +
                                            ((vertex.z - prev_vert.z) ** 2))
            prev_vert = vertex
        
        return distance
