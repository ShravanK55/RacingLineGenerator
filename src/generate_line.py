"""
Script to generate racing lines using genetic algorithms.
"""

import math
import os
import struct

import bmesh
import bpy
from mathutils import Vector

from car import Car
from cma_evolutionary_strategy import CMAEvolutionaryStrategy
from evolutionary_strategy import EvolutionaryStrategy
from lap_time_calculator import LapTimeCalculator
from racing_line import RacingLine
from utils import generate_mesh_from_vertices

TRACK_FILE_NAME = "fast_lane.ai"
BORDER_LEFT_NAME = "border_left6"
BORDER_RIGHT_NAME = "border_right7"

left_lane_name = TRACK_FILE_NAME + "_" + BORDER_LEFT_NAME
right_lane_name = TRACK_FILE_NAME + "_" + BORDER_RIGHT_NAME

left_lane = bpy.data.objects[left_lane_name]
right_lane = bpy.data.objects[right_lane_name]

left_locs = [left_lane.matrix_world @ vertex.co for vertex in left_lane.data.vertices]
right_locs = [right_lane.matrix_world @ vertex.co for vertex in right_lane.data.vertices]
left_line = RacingLine(left_locs)
right_line = RacingLine(right_locs)
car = Car()
lap_time_calculator = LapTimeCalculator()

print("The track distance is " + str(left_line.length) + "m.")
sector_0 = left_line.get_sector(0)
print("Sector 0 radius is: {}".format(sector_0.radius))
print("Sector 0 length is: {}".format(sector_0.length))
print("Sector 0 max speed: {}".format(lap_time_calculator.get_sector_max_velocity(sector_0, car) * 3.6))
print("Sector 0 entry speed: {}".format(lap_time_calculator.get_sector_entry_velocity(sector_0, car, 5.0) * 3.6))
print("Sector 0 exit speed: {}".format(lap_time_calculator.get_sector_exit_velocity(sector_0, car, 0.0) * 3.6))
lap_time = lap_time_calculator.calculate_lap_time(left_line, car, 80.0)
print("Lap time: {}".format(lap_time))

strategy = CMAEvolutionaryStrategy(left_line, right_line, car, starting_velocity=80.0)
best_candidate = strategy.run()
r_line = RacingLine.generate_from_weights(best_candidate.weights, left_line, right_line)
generate_mesh_from_vertices(r_line.vertices)
