"""
Module for racing lines.
"""

import math


class Sector:
    """
    Class representing a sector in a racing line.
    A sector is a path representing by 3 points in space, the start, the middle and an end.
    """
    
    def __init__(self, vertices):
        """
        Method to initialize a sector.
        
        Args:
            vertices(tuple): List of vertices in the sector.

        """
        self.vertices = vertices
        self.start = vertices[0]
        self.mid = vertices[1]
        self.end = vertices[2]
        
    @property
    def radius(self):
        """
        Gets the radius of the path along the sector.
        Reference: http://www.jameshakewill.com/Lap_Time_Simulation.pdf
        
        Returns:
            radius(float): Radius of the sector in metres.

        """
        a = (self.end - self.start).length
        b = (self.end - self.mid).length
        c = (self.mid - self.start).length
        cos_angle = ((c ** 2) + (b ** 2) - (a ** 2)) / (2 * b * c)
        
        if cos_angle > 1:
            cos_angle = 1
        elif cos_angle < -1:
            cos_angle = -1

        sector_angle = math.acos(cos_angle)
        if sector_angle == 0 or sector_angle == math.pi:
            return math.inf
        
        radius = a / (2 * math.sin(math.pi - sector_angle))
        return radius

    @property
    def length(self):
        """
        Gets the length of a sector.
        
        Returns:
            length(float): Length of sector in metres.

        """
        if not self.vertices:
            return 0
        
        length = 0
        prev_vert = self.vertices[0]
        
        for vertex in self.vertices:
            length = length + (vertex - prev_vert).length
            prev_vert = vertex
        
        return length


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

    def get_sector(self, idx):
        """
        Method to get the sector for a given vertex index.
        
        Args:
            idx(int): Index of the vertex to get the sector for.

        Returns:
            sector(Sector): Sector of the given vertex.

        """
        if (idx >= len(self.vertices)):
            idx = idx % len(self.vertices)

        # Given that there are 3 vertices in a sector, the sector index would be a third of the vertex index.
        start_idx = idx - (idx % 3)
        mid_idx = (start_idx + 1) % len(self.vertices)
        end_idx = (start_idx + 2) % len(self.vertices)
        
        sector = Sector([self.vertices[start_idx], self.vertices[mid_idx], self.vertices[end_idx]])
        return sector

    @property
    def sectors(self):
        """
        Method to get all the sectors in a racing line.

        Returns:
            sectors(list): Returns a list of all the sectors in the racing line.

        """
        if not self.vertices:
            return []
        
        sectors = [self.get_sector(i) for i in range(int(len(self.vertices) / 3))]
        return sectors

    @property
    def length(self):
        """
        Gets the length of a racing line.
        
        Returns:
            length(float): Length of racing line in metres.

        """
        if not self.vertices:
            return 0
        
        length = 0
        prev_vert = self.vertices[0]
        
        for vertex in self.vertices:
            length = length + (vertex - prev_vert).length
            prev_vert = vertex
        
        return length
