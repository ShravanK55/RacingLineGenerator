"""
Module for implementing various utility functions.
"""

import bpy
import numpy as np


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


def en0i(n):
    """
    Method to get one of the constants used in the calculation of step size update.
    Refer to https://arxiv.org/pdf/1604.00772.pdf for E||N(0, I)||

    Args:
        n(int): Length of the solution vector.

    Returns:
        en0i(float): Constant involved in the calculation of the step size update.

    """
    return np.sqrt(n) * (1 - 1.0 / (4 * n) + 1.0 / (21 * n * n))


def generate_mesh_from_vertices(vertices, mesh_name="racing_line", collection_name="Collection"):
    """
    Method to generate a mesh in blender from a list of vertex locations.

    Args:
        vertices(list): List of vertices to create the mesh from.
        mesh_name(str): Name of the mesh to be created. Defaults to "racing_line".
        collection_name(str): Name of the collection to add the mesh to. Defaults to "Collection".

    """
    mesh = bpy.data.meshes.new(mesh_name)
    obj = bpy.data.objects.new(mesh.name, mesh)
    col = bpy.data.collections.get(collection_name)
    col.objects.link(obj)

    edges = []
    for idx in range(len(vertices)):
        edges.append([idx, (idx + 1) % len(vertices)])

    mesh.from_pydata(vertices, edges, [])
