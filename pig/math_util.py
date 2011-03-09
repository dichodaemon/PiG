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
  return ( o.x + o.rect.width  * o.pixelSize / 2.0,
           o.y + o.rect.height * o.pixelSize / 2.0
         )

def collisionSide( o1, o2 ):
  r         = o2.rect
  x1        = o1.oldX + o1.rect.width  * o1.pixelSize / 2.0 
  y1        = o1.oldY + o1.rect.height * o1.pixelSize / 2.0
  x2        = o1.x + o1.rect.width  * o1.pixelSize / 2.0 
  y2        = o1.y + o1.rect.height * o1.pixelSize / 2.0 
  x3        = o2.x 
  y3        = o2.y
  x4        = x3 + r.width  * o2.pixelSize
  y4        = y3 + r.height * o2.pixelSize
  dist      = 1E6
  r =  intersection( x1, y1, x2, y2, x3, y3, x3, y4 )
  side      = None
  if r:
    dist = (r[0] - x1) ** 2 + (r[1] - y1) ** 2
    side = "LEFT"
  r = intersection( x1, y1, x2, y2, x4, y3, x4, y4 )
  if r:
    d = (r[0] - x1) ** 2 + (r[1] - y1) ** 2
    if d < dist:
      dist = d
      side = "RIGHT"
  r = intersection( x1, y1, x2, y2, x3, y4, x4, y4 )
  if r:
    d = (r[0] - x1) ** 2 + (r[1] - y1) ** 2
    if d < dist:
      dist = d
      side = "DOWN"
  r = intersection( x1, y1, x2, y2, x3, y3, x4, y3 )
  if r:
    d = (r[0] - x1) ** 2 + (r[1] - y1) ** 2
    if d < dist:
      dist = d
      side = "TOP"
  return side

def autoPush( o1, o2 ):
    side = collisionSide( o1, o2 )
    x1, y1 = realCenter( o1 )
    x2, y2 = realCenter( o2 )
    ix = ( o2.rect.width  * o2.current.pixelSize + o1.rect.width  * o1.current.pixelSize ) / 2.0 - abs( x2 - x1 )
    iy = ( o2.rect.height * o2.current.pixelSize + o1.rect.height * o1.current.pixelSize ) / 2.0 - abs( y2 - y1 )
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
      o2.y += iy * w2
      o1.y -= iy * w1
    elif side == "BOTTOM":
      o2.y -= iy * w2
      o1.y += iy * w1

