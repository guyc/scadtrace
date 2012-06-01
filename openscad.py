import sys

class OpenscadPolyhedron:
    def __init__(self):    
        self.points = []
        self.triangles = []


    def write(self, file=None):
        if file == None:
            file = sys.stdout
            
        file.write("polyhedron (\n")
        file.write("  points = [")
        for point in self.points:
            file.write("[")
            file.write(",".join(map(str,point)))
            file.write("],\n")
        file.write("],\n")
        file.write("  triangles = [")
        for triangle in self.triangles:
            file.write("[")
            file.write(",".join(map(str,triangle)))
            file.write("],\n")
        file.write("]\n")
        file.write(");\n")
