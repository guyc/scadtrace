#!/usr/bin/env python
import sys
import os
import math
from svg import *
from openscad import *
from quake import *

# setting quality=true
# introduces new points on the outer edge of the polygon
# which would be fine BUT openscad barfs presumably because it gets
# rounding error slivers making the polyhedron not so closed.
#
# Seems like the intermediate breaks will be useful for wrapping,
# so instead of looking at options to keep the edge intact, lets
# figure out how to find these edges.

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


def polyhedronFromMesh(z0, z1, mesh):
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
    m = len(mesh.vertices)
    for segment in mesh.segments:
        v1 = segment[0]
        v0 = segment[1]
        v3 = segment[0] + m
        v2 = segment[1] + m

        # order of segments matches order of triangles which is anticlockwise so we reverse it.
        polyhedron.triangles.append([v2,v1,v0])
        polyhedron.triangles.append([v1,v2,v3])

    # front and back face triangles
    for triangle in mesh.triangles:
        # reverse the direction
        polyhedron.triangles.append([triangle[2],triangle[1],triangle[0]])
        polyhedron.triangles.append([triangle[0]+m, triangle[1]+m, triangle[2]+m])
        pass
    
    return polyhedron

def rotateXY(polyhedron):
    for point in polyhedron.points:
        x = point[0]
        y = point[1]
        z = point[2]

        point[0] = y
        point[1] = -x

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
#polygons = polygons[20:21] # something wrong with this one

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

index = 0        
for polygon in polygons:
    #dumpPoints(polygon)
    #print("")

    tri = QuakeTriangle()
    # set options on tri if you want
    tri.quality = True
    
    qp = QuakePolygon()

    # set the vertices and segments for the quake polygon
    # but note that these values may be different in the
    # mesh returned
    qp.vertices = polygon
    n = len(polygon)
    for i in range(0,n):
        qp.segments.append([i,(i+1)%n])
    mesh = tri.polyToMesh(qp,str(index))

    # mesh has triangles and bounding nodes for the face
    # the first len(polygon) points in the vertex list are
    # the original edge points.  Constructing the polyhedron
    # takes a couple of passes

    polyhedron = polyhedronFromMesh(-50,50, mesh)
    if True:
        rotateXY(polyhedron)
        angle = 90
        width = maxy-miny
    else:
        width = maxx-minx

    projectToCylinder(polyhedron, angle, width)
    polyhedron.write(scadFile)
    index+=1

scadFile.close()
