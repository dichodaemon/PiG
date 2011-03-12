# -*- coding:utf-8 -*-

import pig

class Wolverine( pig.Actor ):
  def __init__( self, pixelSize = 1 ):
    pig.Actor.__init__( self )
    self.addView( 
      "right", pig.Animation( "images/wolverine_walking.png", 6, 9, True ) , pixelSize = pixelSize
    )
    self.addView( 
      "left", pig.Animation( "images/wolverine_walking.png", 6, 9, False ) , pixelSize = pixelSize
    )
    self.sign = 1 
    self.vy   = 0
    self.vx   = 1.38
    self.exit = 0

  def update( self, time, elapsed ):
    x, y = self.getPosition()
    x += self.sign * elapsed * self.vx
    y += self.vy   * elapsed
    self.move( x, y )
    if self.y > 0:
      self.vy -= 10 * elapsed
    else:
      self.vy = 0
      self.y  = 0
    return self.exit

  def onKeyDown( self, key ):
    if key == "left":
      self.sign = -1
      self.setView( "left" )
    elif key == "right":
      self.sign = 1
      self.setView( "right" )
    elif key == "up":
      if self.vy == 0:
        self.vy = 7

  def onCollide( self, other ):
    if other.id == "door1":
      self.exit = 1
    elif other.id == "door2":
      self.exit = 2
    c = pig.CollisionInfo( self, other )
    if c.side == "TOP" or c.topOverlap > 0 and c.topOverlap < 0.1:
      self.vy = 0
      c.autoPush( onX = False )
    else:
      c.autoPush()

