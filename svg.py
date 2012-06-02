import xml.dom.minidom 
import re
import string

class SvgState:
  def __init__(self):
    self.x = 0
    self.y = 0
    self.x0 = 0  # opening of path
    self.y0 = 0

class SvgCmd:
  def __init__(self, match):
    self.cmd = match.group(1)
    self.relative = self.cmd.islower()
    if len(match.groups())>1:
      self.setCoords(self.parseCoords(match.group(2)))

  def absolute(self, state, points):
    if self.relative:
      abs = []
      for point in points:
        abs.append([point[0]+state.x, point[1]+state.y])
      return abs
    else:
      return points

  def parseCoords(self, match):
    coords = []
    for coord in re.split('\s+', match.strip()):
      coords.append(float(coord))
    return coords

  def setCoords(self, coords):
    self.coords = coords

  def repack(self, coords, groupSize):
    groups = []
    assert len(coords)%(2*groupSize)==0
    while len(coords)>0:
      group = []
      for i in range(0, groupSize):
        group.append([coords.pop(0),coords.pop(0)])
      groups.append(group)
    return groups

  def pack(self, coords):
    points = []
    assert len(coords)%2 == 0
    while len(coords)>0:
      points.append([coords.pop(0), coords.pop(0)])
    return points

class SvgMoveCmd(SvgCmd):

  def setCoords(self, coords):
    assert len(coords)==2
    self.coords = coords

  def run(self, state):
    coords = self.absolute(state, [self.coords])
    state.x = coords[0][0]
    state.y = coords[0][1]
    state.x0 = state.x  # starts a new subpath
    state.y0 = state.y
    return []

class SvgCurveCmd(SvgCmd):

  def setCoords(self, coords):
    assert (len(coords)%6)==0
    self.curves = self.repack(coords, 3) # each curve has 3 x,y coords

  def run(self, state):
    points = []
    for curve in self.curves:
      points.extend(self.points(state, curve))

    # reset the origin on each C command, not each subcurve!
    #lastCurve = self.curves[len(self.curves)-1]
    #lastPoint = lastCurve[len(lastCurve)-1]
    #state.x = lastPoint[0]
    #state.y = lastPoint[1]
    return points
      
    # ref: http://www.c-sharpcorner.com/uploadfile/apundit/drawingcurves11182005012515am/drawingcurves.aspx
  def points(self, state, curve):
    points = []
    divisions = 10  # REVISIT - determine this automatically

    curve = self.absolute(state, curve)

    p1x = state.x
    p1y = state.y
    p2x = curve[0][0]
    p2y = curve[0][1]
    p3x = curve[1][0]
    p3y = curve[1][1]
    p4x = curve[2][0]
    p4y = curve[2][1]

    points.append([p1x, p1y])
    # http://en.wikipedia.org/wiki/B%C3%A9zier_curve
    for i in range(1,divisions):
      t = float(i) / float(divisions)
      f1 =   (1-t)**3
      f2 = 3*(1-t)**2*t
      f3 = 3*(1-t)   *t*t
      f4 =            t*t*t
      points.append([
        f1 * p1x + f2 * p2x + f3 * p3x + f4 * p4x,
        f1 * p1y + f2 * p2y + f3 * p3y + f4 * p4y
      ])
    points.append([p4x, p4y])

    state.x = p4x
    state.y = p4y
    
    return points

class SvgCloseCmd(SvgCmd):
  def run(self, state):
    state.x = state.x0
    state.y = state.y0
    return [[state.x0,state.y0]]

class SvgLineCmd(SvgCmd):
  def setCoords(self, coords):
    assert(len(coords)%2)==0  # expect x,y pairs
    self.strokes = self.pack(coords)
    
  def run(self, state):
    points = [[state.x,state.y]]
    for stroke in self.strokes:
      absStroke = self.absolute(state, [stroke])
      point = absStroke[0]
      points.append(point)
      state.x = point[0]
      state.y = point[1]
    return points

class Svg:
  def __init__(self, filename):
    self.doc = xml.dom.minidom.parse(filename)
    self.re = {
      # these re's only work for integer coordinates
      'M'    : re.compile('^\s*(M)\s*((-?\d+\s*){2})'),
      'c'    : re.compile('^\s*(c|C)\s*((-?\d+\s*){6,})\s*'),
      'z'    : re.compile('^\s*(z)\s*'),
      'l'    : re.compile('^\s*(l)\s*((-?\d+\s*){2,})\s*'),
    }
    svgNode = self.doc.documentElement
    self.width = int(svgNode.attributes["width"].value.rstrip("pt"))
    self.height = int(svgNode.attributes["height"].value.rstrip("pt"))

  def parsePath(self, pathString):
    cmds = []
    while pathString!="":
      match=self.re['M'].match(pathString)
      if (match):
        cmds.append(SvgMoveCmd(match))     
      else:
        match=self.re['c'].match(pathString)
        if (match):
          cmds.append(SvgCurveCmd(match))
        else:
          match=self.re['z'].match(pathString)
          if (match):
            cmds.append(SvgCloseCmd(match))
          else:
            match=self.re['l'].match(pathString)
            if (match):
              cmds.append(SvgLineCmd(match))
            else:
              raise Exception('Unparseable path string ('+pathString+')')

      # trim whatever was matched
      pathString = match.string[match.end(0):]

    return cmds

  def paths(self):
    paths = []
    for node in self.doc.getElementsByTagName('path'):
      #print(node.toprettyxml())
      d = node.attributes["d"].value
      #print d
      paths.append(self.parsePath(d))
    #print paths
    return paths

  # polygon is [[x,y]...]
  # remove adjacent identical pairs.
  def thin(self, polygon):
      lastCoord = None
      thinPolygon = []
      for coord in polygon:
          if coord != lastCoord:
              thinPolygon.append(coord)
              lastCoord = coord

      # this polygon is implicitly closed, so remove any explicit closure
      if polygon[0]==lastCoord:
          polygon.pop()
          
      return thinPolygon

  def polygons(self):
    polygons = []
    state = SvgState()
    paths = self.paths()
    for path in paths:
      polygon = []
      state.x0 = state.x  # not sure we need this
      state.y0 = state.y
      for cmd in path:
        polygon.extend(cmd.run(state))
      polygons.append(self.thin(polygon))
    return polygons
