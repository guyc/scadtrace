import subprocess
import re
# By default, Triangle copies all
# vertices in the input .node file to the output .node file, in the
# same order, so their indices do not change.

class QuakeTriangle:
    def __init__(self):
        self.quality = True
        self.triangle = "/Users/guy/src/triangle/triangle"

    def polyToMesh(self,poly):
        base = "/tmp/triangle" # REVISIT - use tmpnam
        poly.writePoly(base+".poly")
        # -I supresses iteration numbers in output file names
        # -z uses 0-based numbering
        cmd = [self.triangle,"-I","-z"]
        if self.quality:
            cmd += ["-q"]
        cmd += ["-p", base+".poly"]
        print cmd
        result = subprocess.call(cmd)
        mesh = QuakeMesh()
        mesh.readEle(base+".ele")
        mesh.readNode(base+".node")
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
        line = lines.pop(0)    
        noHoles = int(line[0])

        self.holes = []
        for i in range(0,noHoles):
            line = lines.pop(0)
            self.holes.append([line[1], line[2]])

        print lines

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
        
class QuakeMesh(QuakeGeom):

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
        
