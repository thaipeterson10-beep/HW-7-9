#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 11:25:01 2021

@author: kendrick shepherd
"""

import math
import numpy as np
import sys

# length of the beam
def Length(bar):
    # find a node of the bar
    bar_node = bar.init_node
    # convert the node and bar to a vector
    vector = BarNodeToVector(bar_node, bar)
    # find the length of the vector
    bar_length = VectorTwoNorm(vector)
    # output the vector length
    return bar_length

# Find two norm (magnitude) of a vector
def VectorTwoNorm(vector):
    norm = 0
    for i in range(0, len(vector)):
        norm += vector[i]**2
    return np.sqrt(norm)

# Find a shared node between two bars
def FindSharedNode(bar_1,bar_2):
    if(bar_1.init_node==bar_2.init_node):
        return bar_1.init_node
    elif bar_1.init_node == bar_2.end_node:
        return bar_1.init_node
    elif bar_1.end_node == bar_2.init_node:
        return bar_1.end_node
    elif bar_1.end_node == bar_2.end_node:
        return bar_1.end_node
    # the bars do not share a common node
    #output an error---you should never arrive here
    else:
        sys.exit("The two input bars do not share a node")
    

# Given a bar and a node on that bar, find the other node
def FindOtherNode(node,bar):
    if(bar.init_node == node):
        return bar.end_node
    elif(bar.end_node == node):
        return bar.init_node
    else:
        sys.exit("The input node is not on the bar")

# Find a vector from input node (of the input bar) in the direction of the bar
def BarNodeToVector(origin_node,bar):
    other_node = FindOtherNode(origin_node, bar)
    origin_loc = origin_node.location
    other_loc = other_node.location
    vec = [other_loc[0]-origin_loc[0], other_loc[1]-origin_loc[1]]
    return vec

# Convert to bars that meet at a node into vectors pointing away from that node
def BarsToVectors(bar_1,bar_2):
    shared_node = FindSharedNode(bar_1, bar_2)

    # Determine the far node for bar_1
    if bar_1.init_node == shared_node:
      bar_1_other = bar_1.end_node
    else:
      bar_1_other = bar_1.init_node

    # Determine the far node for bar_2
    if bar_2.init_node == shared_node:
      bar_2_other = bar_2.end_node
    else:
      bar_2_other = bar_2.init_node

    # Vector pointing from shared node to the other node for each bar
    vec_1 = np.array([
        bar_1_other.x - shared_node.x,
        bar_1_other.y - shared_node.y,
        bar_1_other.z - shared_node.z,
    ])
    vec_2 = np.array([
        bar_2_other.x - shared_node.x,
        bar_2_other.y - shared_node.y,
        bar_2_other.z - shared_node.z,
    ])

    return vec_1, vec_2

# Cross product of two vectors
def TwoDCrossProduct(vec1,vec2):
    return vec1[0] * vec2[1] - vec1[1] * vec2[0]

# Dot product of two vectors
def DotProduct(vec1, vec2):
    return sum(v1 * v2 for v1, v2 in zip(vec1, vec2))

# Cosine of angle from local x vector direction to other vector
def CosineVectors(local_x_vec,other_vec):
    dot_product = DotProduct(local_x_vec, other_vec)
    magnitude_product = VectorTwoNorm(local_x_vec) * VectorTwoNorm(other_vec)
    return dot_product / magnitude_product

# Sine of angle from local x vector direction to other vector
def SineVectors(local_x_vec,other_vec):
    cross_prod = TwoDCrossProduct(local_x_vec, other_vec)
    norm_product = VectorTwoNorm(local_x_vec) * VectorTwoNorm(other_vec)
    return cross_prod / norm_product


# Cosine of angle from local x bar to the other bar
def CosineBars(local_x_bar,other_bar):
  # Convert bars into directional vectors pointing away from the shared node
  vec_1, vec_2 = BarsToVectors(local_x_bar, other_bar)

  # Compute dot product and magnitudes
  dot_product = np.dot(vec_1, vec_2)
  norm_1 = np.linalg.norm(vec_1)
  norm_2 = np.linalg.norm(vec_2)

  # Cosine of the angle between the two vectors
  cos_theta = dot_product / (norm_1 * norm_2)

  return cos_theta
    

# Sine of angle from local x bar to the other bar
def SineBars(local_x_bar,other_bar):
  # Convert bars into directional vectors pointing away from the shared node
  vec_1, vec_2 = BarsToVectors(local_x_bar, other_bar)

  # Compute cross product and magnitudes
  cross_product = np.cross(vec_1, vec_2)
  norm_cross = np.linalg.norm(cross_product)
  norm_1 = np.linalg.norm(vec_1)
  norm_2 = np.linalg.norm(vec_2)

  # Sine of the angle between the two vectors
  sin_theta = norm_cross / (norm_1 * norm_2)

  return sin_theta
