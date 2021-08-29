"""
Module for racing lines.
"""

import math

from utils import clamp


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

    @staticmethod
    def generate_from_weights(weights, left_limit, right_limit):
        """
        Method to generate a racing line from weights (Refer to the evolutionary_strategy module).
        NOTE: This method assumes that the length of the weights, left track limit vertices and right track limit
        vertices are the same. The method may not work as expected if they are not.

        Args:
            weights(list): List of weights, each of which range from [0.0, 1.0].
            left_limit(RacingLine): Left side track limit.
            right_limit(RacingLine): Right side track limit.

        Returns:
            racing_line(RacingLine): A racing line generated from the weights and the track limits.

        """
        l_verts = left_limit.vertices
        r_verts = right_limit.vertices
        vertices = []

        for idx in range(len(l_verts)):
            t_vec = r_verts[idx] - l_verts[idx]
            weight = clamp(weights[idx], 0.0, 1.0)
            vert = l_verts[idx] + (t_vec * weight)
            vertices.append(vert)

        racing_line = RacingLine(vertices)
        return racing_line

    def get_sector(self, idx):
        """
        Method to get the sector at a given index.

        Args:
            idx(int): Index of the the sector to get.

        Returns:
            sector(Sector): Sector of the given index.

        """
        if (idx >= int(len(self.vertices) / 2)):
            idx = idx % int((len(self.vertices) / 2))

        # Given that there are 3 vertices in a sector, the sector index would be a third of the vertex index.
        start_idx = idx * 2
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

        sectors = []
        idx = 0
        for _ in range(0, len(self.vertices), 2):
            sector = self.get_sector(idx)
            sectors.append(sector)
            idx = idx + 1

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
