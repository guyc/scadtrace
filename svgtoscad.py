#!/usr/bin/env python
import sys
import os
import math
from svg import *
from openscad import *
from quake import *


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


def polyhedronFromMesh(z0, z1, mesh, noEdgePoints):
    polyhedron = OpenscadPolyhedron()

    # z0 points
    for vertex in mesh.vertices:
        x = vertex[0]
        y = vertex[1]
        polyhedron.points.append([x,y,z0])
    # z1 points
    for vertex in mesh.vertices:
        x = vertex[0]
        y = vertex[1]
        polyhedron.points.append([x,y,z1])
    # trangles for edge faces
    n = noEdgePoints
    m = len(mesh.vertices)
    for i in range(0,n):
        polyhedron.triangles.append([i,(i+1)%n,i+m])
        polyhedron.triangles.append([i+m, (i+1)%n, (i+1)%n+m])

    print noEdgePoints
    print len(mesh.vertices)
    print len(polyhedron.points)
    print len(polyhedron.triangles)
    
        
    # front and back face triangles
    for triangle in mesh.triangles:
        # reverse the direction
        polyhedron.triangles.append([triangle[2],triangle[1],triangle[0]])
        polyhedron.triangles.append([triangle[0]+m, triangle[1]+m, triangle[2]+m])

    return polyhedron

#  The target object is centered at the origin
#  We will reproject it to a cylinder around the Y axis
#  with the given radius.  Scale will be preserved at the
#  Y-Z plane.
def projectToCylinder(polyhedron, angle, width):

  # pick a radius so that the width with span the angle
  # angle / 180 * 2 is the fraction of the circumference we want to span
  # circum = 2 pi R
  # R = circum / 2pi
  circum = width * 360 / angle
  radius = circum / (2 * math.pi)
    
  for point in polyhedron.points:
      x0 = point[0]
      y0 = point[1]
      z0 = point[2]
      # map to polar coordinates
      a = x0 * angle / width * math.pi / -180.0
      r = radius + z0
      # 
      x1 = -math.sin(a) * r
      y1 = y0
      z1 = math.cos(a) * r
      point[0] = x1
      point[1] = y1
      point[2] = z1
      
scadFile = open("artwork.scad", "w") # hack

svg = Svg(filename)

polygons = svg.polygons()
#polygons = polygons[0:10] # HACK FOR TESTING

# center the polygon
minx = maxx = polygons[0][0][0]
miny = maxy = polygons[0][0][1]
for polygon in polygons:
    for point in polygon:
        x = point[0]
        if x < minx:
            minx = x 
        if x > maxx:
            maxx = x
        y = point[1]
        if y < miny:
            miny = y 
        if y > maxy:
            maxy = y

for polygon in polygons:
    for point in polygon:
        point[0] -= minx + (maxx-minx)/2
        point[1] -= miny + (maxy-miny)/2
        
for polygon in polygons:
    #dumpPoints(polygon)
    #print("")

    #polygon = polygon[0:5]  # HACK FOR TESTING

    tri = QuakeTriangle()
    # set options on tri if you want
    tri.quality = True
    
    qp = QuakePolygon()
    qp.vertices = polygon
    n = len(polygon)
    for i in range(0,n):
        qp.segments.append([i,(i+1)%n])
    mesh = tri.polyToMesh(qp)

    # mesh has triangles and bounding nodes for the face
    # the first len(polygon) points in the vertex list are
    # the original edge points.  Constructing the polyhedron
    # takes a couple of passes

    polyhedron = polyhedronFromMesh(-50,50, mesh, len(polygon))

    angle = 180
    width = maxx-minx
    projectToCylinder(polyhedron, angle, width)
    polyhedron.write(scadFile)

scadFile.close()
