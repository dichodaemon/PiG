# -*- coding:utf-8 -*-

import pig
import pygame

class Slinky( pig.Actor ):
  def __init__( self, pixelSize = 1 ):
    pig.Actor.__init__( self )
    # Load separate images for every frame 
    # (we are going to animated them by hand)
    self.addView( 
      "r1", pig.Image( "images/slinky1.png" ) , pixelSize = pixelSize
    )
    self.addView( 
      "r2", pig.Image( "images/slinky2.png" ) , pixelSize = pixelSize
    )
    self.addView( 
      "r3", pig.Image( "images/slinky3.png" ) , pixelSize = pixelSize
    )
    self.addView( 
      "l1", pig.Image( "images/slinky1.png", True ) , pixelSize = pixelSize
    )
    self.addView( 
      "l2", pig.Image( "images/slinky2.png", True ) , pixelSize = pixelSize
    )
    self.addView( 
      "l3", pig.Image( "images/slinky3.png", True ) , pixelSize = pixelSize
    )
    self.setView( "r3" )
    # Setup initial velocity and facing direction
    self.vx    = 0
    self.vy    = 0
    self.d     = "r"
    # Slinky will start out falling
    self.state = "FALLING"
    self.sound  = pygame.mixer.Sound( "sounds/boink.wav" )

  def update( self, time, elapsed ):
    if self.state == "START_JUMP": # Start measuring time from jump start
      self.jumpTime = time
      self.state = "JUMPING"
      self.playing = False
    elif self.state == "JUMPING":  # Depending on time from jump start
      t = time - self.jumpTime
      if t > 0.5:                    
        self.setView( self.d + "3" ) # Set state as falling and increase vertical
        self.state = "FALLING"       # velocity
        self.vy    = 8
        # If the platform we are leaving is breakable, remove it
        if self.platform.id == "breakable":
          self.platform.remove = True
      elif t > 0.35:                 # Just choose the appropriate frame 
        self.setView( self.d + "2" )
      elif t > 0.20:
        self.setView( self.d + "1" )
      elif t > 0.05:
        if not self.playing:
          self.sound.play()
          self.playing = True
        self.setView( self.d + "2" )
      else:
        self.setView( self.d + "3" )
    else:                           # If slinky is falling
      self.setView( self.d + "3" )  # Face the current direction
      self.y  += elapsed * self.vy  # Update position and vertical velocity
      self.vy -= 0.2
      self.x  += elapsed * self.vx

  def onKeyDown( self, key ):
    # Set the facing direction and horizontal velocity depending on the
    # input key
    if key == "left":
      self.vx = -1.5
      self.d  = "l"
    elif key == "right":
      self.vx = 1.5
      self.d  = "r"

  def onKeyUp( self, key ):
    # If the key is not being pressed anymore, stop moving horizontally
    if key == "left" or key == "right":
      self.vx = 0

  def onCollide( self, other ):
    # For now, we can only collide on platforms
    c = pig.CollisionInfo( self, other )
    if (      c.side == "TOP" and self.state == "FALLING" 
          and self.vy < 0   and abs( self.y - other.y ) < 0.05 ):
      self.state    = "START_JUMP"
      self.platform = other
      c.autoPush()
