# -*- coding: utf-8 -*-

class CollisionInfo( object ):
  def __init__( self, o1, o2 ):
    self.o1 = o1
    self.o2 = o2
    r1 = o1.rect
    r2 = o2.rect
    x  = o1.oldX + r1.width  / 200.0
    y  = o1.oldY + r1.height / 200.0
    x1 = o1.x
    y1 = o1.y
    x2 = x1 + r1.width  / 100.0
    y2 = y1 + r1.height / 100.0
    x3 = o2.x 
    y3 = o2.y
    x4 = x3 + r2.width  / 100.0
    y4 = y3 + r2.height / 100.0
    self.leftOverlap   = 0
    self.rightOverlap  = 0
    self.topOverlap    = 0
    self.bottomOverlap = 0
    self.side = ""
    dist = 1E6
    if x < x3:
      d = x2 - x3
      dist = abs( d )
      self.side = "LEFT"
      if x2 > x3:
        self.leftOverlap = d
    if y < y3:
      d = y2 - y3
      if abs( d ) < dist:
        dist = abs( d )
        self.side = "BOTTOM"
      if y2 > y3:
        self.bottomOverlap = d
    if x > x4:
      d = x4 - x1
      if abs( d ) < dist:
        dist = abs( d )
        self.side = "RIGHT"
      if x4 > x1:
        self.rightOverlap = d
    if y > y4:
      d = y4 - y1
      if abs( d ) < dist:
        dist = abs( d )
        self.side = "TOP"
      if y4 > y1:
        self.topOverlap = d
    self.overlap = (
      self.leftOverlap,
      self.rightOverlap,
      self.topOverlap,
      self.bottomOverlap
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

