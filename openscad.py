import sys

class OpenscadPolyhedron:
    def __init__(self):    
        self.points = []
        self.triangles = []


    def render(self):
        sys.stdout.write("polyhedron (\n")
        sys.stdout.write("  points = [")
        for point in self.points:
            sys.stdout.write("[")
            sys.stdout.write(",".join(map(str,point)))
            sys.stdout.write("],")
        sys.stdout.write("],\n")
        sys.stdout.write("  triangles = [")
        for triangle in self.triangles:
            sys.stdout.write("[")
            sys.stdout.write(",".join(map(str,triangle)))
            sys.stdout.write("],")
        sys.stdout.write("]\n")
        sys.stdout.write(");\n")
