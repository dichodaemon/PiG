# -*- coding: utf-8 -*-

class CollisionInfo( object ):
  def __init__( self, o1, o2 ):
    self.o1 = o1
    self.o2 = o2
    r1 = o1.rect
    r2 = o2.rect
    dx1 = o1.x - o1.oldX
    dy1 = o1.y - o1.oldY
    dz1 = o1.z - o1.oldZ
    dx2 = o2.x - o2.oldX
    dy2 = o2.y - o2.oldY
    dz2 = o2.z - o2.oldZ
    x  = o1.oldX + r1.width  / 200.0
    y  = o1.oldY + r1.height / 200.0
    z  = o1.oldZ
    x1 = o1.x
    y1 = o1.y
    z1 = o1.z - o1.thickness / 2.0
    x2 = x1 + r1.width  / 100.0
    y2 = y1 + r1.height / 100.0
    z2 = o1.z + o1.thickness / 2.0
    x3 = o2.x 
    y3 = o2.y
    z3 = o2.z - o2.thickness / 2.0
    x4 = x3 + r2.width  / 100.0
    y4 = y3 + r2.height / 100.0
    z4 = o2.z + o2.thickness / 2.0

    self.leftOverlap   = 0
    self.rightOverlap  = 0
    self.topOverlap    = 0
    self.bottomOverlap = 0
    self.frontOverlap  = 0
    self.backOverlap   = 0

    self.side = ""
    dist = 1E6

    if x2 > x3:
      self.leftOverlap = x2 - x3
    if y2 > y3:
      self.bottomOverlap = y2 - y3
    if z2 > z3:
      self.frontOverlap = z2 - z3
    if x1 < x4:
      self.rightOverlap = x4 - x1
    if y1 < y4:
      self.topOverlap = y4 - y1
    if z1 < z4:
      self.backOverlap = z4 - z1

    if x < x3 and dx1 - dx2 > 0:
      d = abs( x2 - x3 )
      dist = d
      self.side = "LEFT"
    if x > x4 and dx2 - dx1 > 0:
      d = abs( x4 - x1 )
      if d < dist:
        dist = d
        self.side = "RIGHT"
    if y < y3 and dy1 - dy2 > 0 :
      d = abs( y2 - y3 )
      if d < dist:
        dist = d
        self.side = "BOTTOM"
    if y > y4 and dy2 - dy1 > 0:
      d = abs( y4 - y1 )
      if d < dist:
        dist = d
        self.side = "TOP"
    if z < z3 and dz1 - dz2 > 0 :
      d = abs( z2 - z3 )
      if d < dist:
        dist = d
        self.side = "FRONT"
    if z > z4 and dz2 - dz1 > 0:
      d = abs( z4 - z1 )
      if d < dist:
        dist = d
        self.side = "BACK"

    self.overlap = (
      self.leftOverlap,
      self.rightOverlap,
      self.topOverlap,
      self.bottomOverlap,
      self.frontOverlap,
      self.backOverlap
    )

  def autoPush( self, onX = True, onY = True ):
    w1 = None
    w2 = None
    if hasattr( self.o1, "weight" ):
      w1 = self.o1.weight
    if hasattr( self.o2, "weight" ):
      w2 = self.o2.weight
    if not w1 and not w2:
      w1 = 1
      w2 = 1
    elif not w1:
      w1 = 1
      w2 = 0
    elif not w2:
      w1 = 0
      w2 = 1
    s = 1.0 * ( w1 + w2 )
    tmp = w1
    w1 = w2  / s 
    w2 = tmp / s

    if onX and onY:
      if (   ( self.leftOverlap + self.rightOverlap )
           > ( self.topOverlap + self.bottomOverlap )  ):
        onY = False
      else:
        onX = False

    if onX:
      if self.leftOverlap > 0:
        self.o2.x += self.leftOverlap * w2
        self.o1.x -= self.leftOverlap * w1
      elif self.rightOverlap > 0:
        self.o2.x -= self.rightOverlap * w2
        self.o1.x += self.rightOverlap * w1
    if onY:
      if self.topOverlap > 0:
        self.o2.y -= self.topOverlap * w2
        self.o1.y += self.topOverlap * w1
      if self.bottomOverlap > 0:
        self.o2.y += self.bottomOverlap * w2
        self.o1.y -= self.bottomOverlap * w1

