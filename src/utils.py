"""
Module for implementing various utility functions.
"""

import bpy


def clamp(value, min_value, max_value):
    """
    Method to clamp a value between a certain range.

    Args:
        value(float): Value to clamp.
        min_value(float): Minimum limit to clamp the value with.
        max_value(float): Upper limit to clamp the value with.

    Returns:
        value(float): Value clamped between the maximum and minimum values.

    """
    return max(min(value, max_value), min_value)


def generate_mesh_from_vertices(vertices, mesh_name="racing_line"):
    """
    Method to generate a mesh in blender from a list of vertex locations.

    Args:
        vertices(list): List of vertices to create the mesh from.
        mesh_name(str): Name of the mesh to be created. Defaults to "racing_line".

    """
    mesh = bpy.data.meshes.new(mesh_name)  # add the new mesh
    obj = bpy.data.objects.new(mesh.name, mesh)
    col = bpy.data.collections.get("Collection")
    col.objects.link(obj)

    edges = []
    for idx in range(len(vertices)):
        edges.append([idx, (idx + 1) % len(vertices)])

    mesh.from_pydata(vertices, edges, [])
