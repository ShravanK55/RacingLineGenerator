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
