"""
Script to generate racing lines using genetic algorithms.
"""

import bpy, bmesh, os, struct, math
from mathutils import Vector


TRACK_FILE_NAME = "fast_lane.ai"
BORDER_LEFT_NAME = "border_left6"
BORDER_RIGHT_NAME = "border_right7"

left_lane_name = TRACK_FILE_NAME + "_" + BORDER_LEFT_NAME
right_lane_name = TRACK_FILE_NAME + "_" + BORDER_RIGHT_NAME

left_lane = bpy.data.objects[left_lane_name]
right_lane = bpy.data.objects[right_lane_name]

left_loc = left_lane.matrix_world @ left_lane.data.vertices[0].co
right_loc = right_lane.matrix_world @ right_lane.data.vertices[0].co

left_locs = [left_lane.matrix_world @ vertex.co for vertex in left_lane.data.vertices]
left_line = RacingLine(left_locs)

print("The track distance is " + str(left_line.length) + "m.")
sector_0 = left_line.get_sector(0)
print("Vertex 0 radius is: {}".format(sector_0.radius))
