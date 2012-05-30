#!/usr/bin/env python
import sys
import os
from svg import *
from openscad import *
import math

filename = sys.argv[1]
if not os.path.exists(filename):
  raise Exception('File not found: '+filename)

def dumpPoints(points):
  for point in points:
    print point[0],",",point[1]

    #
    #path = svg.parsePath("M100 200 C100 100 400 100 400 200")
    #state = SvgState()
    #points = []
    #print path
    #for cmd in path:
    #ext = cmd.run(state)
    #points.extend(ext)
    #dumpPoints(points)


# projection will be
#  - the angle will subtend the entire width (passed as a parameter)
#  - the height of the cylinder will be such that it maintains aspect
#  - the axis is vertical
#  - not sure how to triangulate the surface polygon!  Do I have to?
#  
def projectCylinder(innerRadius, outerRadius, angle, width, polygon):
  polyhedron = OpenscadPolyhedron()
  n = len(polygon)
  i = 0
  # projected width dist is 2.Pi.r * angle / 360 * width
  # use avg of inner and outer radius
  # 
  projX = 2 * math.pi * (innerRadius+outerRadius)/2 * angle / 360.0
  yScale = projX / width
  for point in polygon:
    x = point[0]
    y = point[1]
    a = x * angle / width * math.pi / -180.0 # reverse direction to preserve left-right orientation
    x0 = math.sin(a) * innerRadius
    y0 = math.cos(a) * innerRadius
    z0 = y * yScale
    x1 = math.sin(a) * outerRadius
    y1 = math.cos(a) * outerRadius
    z1 = y * yScale
    m = len(polyhedron.points) # index of p0
    polyhedron.points.append([x0,y0,z0])
    polyhedron.points.append([x1,y1,z1])
    polyhedron.triangles.append([m, m+1, (m+3)%(n*2)])
    polyhedron.triangles.append([(m+3)%(n*2), (m+2)%(n*2), m]) # face rectangle

  #polyhedron.triangles.append(range(0,n*2  ,2))
  #polyhedron.triangles.append(range(1,n*2+2,2)) # todo - reverse this

  return polyhedron
     
    
svg = Svg(filename)

for polygon in svg.polygons():
    #dumpPoints(polygon)
    #print("")
    polyhedron = projectCylinder(100,110,180,4000,polygon)
    polyhedron.render()

