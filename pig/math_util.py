# -*- coding: utf-8 -*-

def lerp( v1, v2, length, progress ):
  f = progress / length
  if f > 1:
    f = 1
  return [ v1[i] + (v2[i] - v1[i]) * f for i in xrange( len( v1 ) ) ]

def intersection( x1, y1, x2, y2, x3, y3, x4, y4 ):
  d  = ( y4 - y3 ) * ( x2 - x1 ) - ( x4 - x3 ) * ( y2 - y1 )
  if d == 0: 
    return None
  n1 = ( x4 - x3 ) * ( y1 - y3 ) - ( y4 - y3 ) * ( x1 - x3 )
  n2 = ( x2 - x1 ) * ( y1 - y3 ) - ( y2 - y1 ) * ( x1 - x3 )
  ua = n1 / d
  ub = n2 / d
  if ub < 0 or ub > 1:
    return None
  return x1 + ua * ( x2 - x1 ), y1 + ua * ( y2 - y1 )  

def realCenter( o ):
  return ( o.x + o.rect.width  / 200.0,
           o.y + o.rect.height / 200.0
         )

def collisionSide( o1, o2 ):
  r1        = o1.rect
  r2        = o2.rect
  x         = o1.oldX + r1.width  / 200.0
  y         = o1.oldY + r1.height / 200.0
  x1        = o1.x
  y1        = o1.y
  x2        = x1 + r1.width  / 100.0
  y2        = y1 + r1.height / 100.0
  x3        = o2.x 
  y3        = o2.y
  x4        = x3 + r2.width  / 100.0
  y4        = y3 + r2.height / 100.0

  dist = 1E6
  side = "None"

  if x < x3:
    dist = x3 - x2
    side = "LEFT"
  if y < y3:
    d = y3 - y2
    if d < dist:
      dist = d
      side = "BOTTOM"
  if x > x4:
    d = x1 - x4
    if d < dist:
      dist = d
      side = "RIGHT"
  if y > y4:
    d = y1 - y4
    if d < dist:
      dist = d
      side = "TOP"
  return side

def autoPush( o1, o2 ):
  side = collisionSide( o1, o2 )
  x1, y1 = realCenter( o1 )
  x2, y2 = realCenter( o2 )
  ix = ( o2.rect.width  + o1.rect.width   ) / 200.0 - abs( x2 - x1 )
  iy = ( o2.rect.height + o1.rect.height  ) / 200.0 - abs( y2 - y1 )
  w1 = None
  w2 = None
  if hasattr( o1, "weight" ):
    w1 = o1.weight
  if hasattr( o2, "weight" ):
    w2 = o2.weight


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

  if side == "LEFT":
    o2.x += ix * w2
    o1.x -= ix * w1
  elif side == "RIGHT":
    o2.x -= ix * w2
    o1.x += ix * w1
  elif side == "TOP":
    o2.y -= iy * w2
    o1.y += iy * w1
  elif side == "BOTTOM":
    o2.y += iy * w2
    o1.y -= iy * w1

