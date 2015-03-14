import subprocess
import re
from sets import Set

# By default, Triangle copies all
# vertices in the input .node file to the output .node file, in the
# same order, so their indices do not change.

class QuakeTriangle:
    def __init__(self):
        self.quality = True
        self.triangle = "./triangle/triangle"

    def polyToMesh(self,poly,suffix=''):
        base = "/tmp/triangle" # REVISIT - use tmpnam
        poly.writePoly(base+".1.poly")
        cmd = [self.triangle]
        # -I supresses iteration numbers in output file names
        # cmd += ["-I"]
        # -z uses 0-based numbering
        cmd += ["-z"]
        if self.quality:
            cmd += ["-q"]
        cmd += ["-p", base+".1.poly"]
        print cmd
        result = subprocess.call(cmd)
        mesh = QuakeMesh()
        # The polygon written back out may have additional boundary points
        # inserted.  We should use that geometry and dump the originally specified 
        # one.
        mesh.readPoly(base+".2.poly")  # populates segments (boundary), clears vertices
        mesh.readNode(base+".2.node") # populates vertices
        mesh.readEle(base+".2.ele") # populates triangles
        # we actually discard the segments and regenerate them here
        mesh.generateSegments()

        return mesh
    
class QuakeGeom:
        
    def readLines(self, filename):
        file = open(filename)
        lines = []
        for line in file:
            if re.match("^\s*($|#)", line):
                pass
            else:
                numbers=map(float, line.split())
                lines.append(numbers)
        file.close
        return lines

    # for some reason segments are not in a
    # predictable order.  Restring them into
    # a continuous string
    def orderSegments(self, segments):
        ordered = []
        while len(segments)>0:
            # print "starting new chain"
            segment = segments.pop(0)
            ordered.append(segment)
            done = False
            while not done:
                done = True
                for i in range(0,len(segments)):
                    if segment[1] == segments[i][0]:
                        #print "found ordered pair at {0}".format(i)
                        segment = segments.pop(i)
                        ordered.append(segment)
                        done = False
                        break
                    elif segment[1] == segments[i][1]:
                        #print "found misordered pair at {0}".format(i)
                        segment = segments.pop(i)
                        segment[0],segment[1] = segment[1],segment[0]
                        ordered.append(segment)
                        done = False
                        break
        return ordered    

    # grrr - to generate the segements from the triangles we need to distinguish
    # which two sides of a triangle with three points marked as boundary vertices
    # are in the boundary.  We elimate pairs which appear both forward and reverse.
    
    def generateSegments(self):
        # using self.triangles (that have reliable winding order)
        # and self.vertices with a boundary indicator
        # reconstruct segments[] to identify all of the line segments
        # along the border in the same winding order as the triangles (which
        # is counter-clockwise

        segForward = Set()
        segReverse = Set()
        for triangle in self.triangles:
            for t0 in range(0,3):
                v0 = triangle[ t0]
                v1 = triangle[(t0+1)%3]
                if self.vertices[v0][2]==1.0 and self.vertices[v1][2]==1.0:
                    segForward.add(tuple([v0,v1]))
                    segReverse.add(tuple([v1,v0]))

        segments = list(segForward-segReverse)

        # even though orderSegments could reverse the order of the vertex pairs,
        # I assert it never will because the order of the first segment dictates
        # the remainder.  In fact because we are passing tuples, the current
        # implementation of orderSegments will crash if it tries to reverse the
        # order of an immutable tuple.
        self.segments = self.orderSegments(segments)

class QuakePolygon(QuakeGeom):

    def __init__(self, filename=None):
        self.dim = 2
        self.noAttributes = 0
        self.noVertexMarkers = 0
        self.vertices = []
        self.noSegmentMarkers = 0
        self.segments = []
        self.holes = []
        
        if filename:
            self.readPoly(filename)

    def readPoly(self, filename):
        lines = self.readLines(filename)

        line = lines.pop(0)
        noVertices          = int(line[0])
        self.dim            = int(line[1])  # must be 2
        self.noAttributes   = int(line[2])
        self.noVertexMarkers= int(line[3])

        self.vertices = []
        for i in range(0,noVertices):
            line = lines.pop(0)
            index = line.pop(0) # ignore id
            self.vertices.append(line) # keep x,y and attributes

        line = lines.pop(0)
        noSegments             = int(line[0])
        self.noSegmentMarkers  = int(line[1])
        self.segments = []
        for i in range(0,noSegments):
            line = lines.pop(0)
            index = line.pop(0)
            a = int(line.pop(0))
            b = int(line.pop(0))
            self.segments.append([a,b]+line) # cast segments to ints
        self.segments = self.orderSegments(self.segments)
        line = lines.pop(0)    
        noHoles = int(line[0])

        self.holes = []
        for i in range(0,noHoles):
            line = lines.pop(0)
            self.holes.append([line[1], line[2]])

    # First line: <# of vertices> <dimension (must be 2)> <# of attributes> <# of boundary markers (0 or 1)>
    # Following lines: <vertex #> <x> <y> [attributes] [boundary marker]
    # One line: <# of segments> <# of boundary markers (0 or 1)>
    # Following lines: <segment #> <endpoint> <endpoint> [boundary marker]
    # One line: <# of holes>
    # Following lines: <hole #> <x> <y>
    # Optional line: <# of regional attributes and/or area constraints>
    # Optional following lines: <region #> <x> <y> <attribute> <maximum area>
    def writePoly(self, filename):
        file = open(filename, "w")

        file.write("{0} {1} {2} {3}\n".format(len(self.vertices), 2, self.noAttributes, self.noVertexMarkers))
        n = 0
        for vertex in self.vertices:
            file.write("{0} ".format(n))
            file.write(" ".join(map(str,vertex)))
            file.write("\n")
            n+=1

        file.write("{0} {1}\n".format(len(self.segments), self.noSegmentMarkers))
        n = 0
        for segment in self.segments:
            file.write("{0} ".format(n))
            file.write(" ".join(map(str,segment)))
            file.write("\n")
            n+=1

        file.write("{0}\n".format(len(self.holes)))
        n = 0
        for hole in self.holes:
            file.write("{0} ".format(n))
            file.write(" ".join(map(str,hole)))
            file.write("\n")
            n+=1
            
        file.close()
        
class QuakeMesh(QuakePolygon):

    # First line: <# of triangles> <nodes per triangle> <# of attributes>
    # Remaining lines: <triangle #> <node> <node> <node> ... [attributes]
    def readEle(self, filename):
        lines = self.readLines(filename)

        line = lines.pop(0)
        noTriangles       = int(line[0])
        self.noAttributes = int(line[1])

        self.triangles = []
        for i in range(0,noTriangles):
            line = lines.pop(0)
            index = line.pop(0) # ignored
            a = int(line.pop(0))
            b = int(line.pop(0))
            c = int(line.pop(0))
            self.triangles.append([a,b,c]+line) # keep attributes

    # First line: <# of vertices> <dimension (must be 2)> <# of attributes> <# of boundary markers (0 or 1)>
    # Remaining lines: <vertex #> <x> <y> [attributes] [boundary marker]
    
    def readNode(self, filename):
        lines = self.readLines(filename)
        line = lines.pop(0)
        noVertices          = int(line[0])
        self.dim            = int(line[1])  # must be 2
        self.noAttributes   = int(line[2])
        self.noVertexMarkers= int(line[3])

        self.vertices = []
        for i in range(0,noVertices):
            line = lines.pop(0)
            index = line.pop(0) # ignore id
            self.vertices.append(line) # keep x,y and attributes
        
