import sys

class OpenscadPolyhedron:
    def __init__(self):    
        self.points = []
        self.triangles = []


    def write(self, file=None):
        if file == None:
            file = sys.stdout
            
        file.write("polyhedron (\n")
        file.write("  points = [ // {0} points\n".format(len(self.points)))
        n = 0
        for point in self.points:
            file.write("[")
            file.write(",".join(map(str,point)))
            file.write("], // {0}\n".format(n))
            n+=1
        file.write("],\n")
        file.write("  triangles = [ // {0} triangles\n".format(len(self.triangles)))
        n = 0
        for triangle in self.triangles:
            file.write("[")
            file.write(",".join(map(str,triangle)))
            file.write("], // {0}\n".format(n))
            n+=1
        file.write("]\n")
        file.write(");\n")
