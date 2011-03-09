# -*- coding:utf-8 -*-

import random
import pygame
import pig
from slinky import *

class JumpScene( pig.Scene ):
  def __init__( self, width, height ):
    pig.Scene.__init__( self, width, height )
    self.camera = pig.Camera( self, width, height, focalLength = 0.035, zOffset = 0 )

    # Create our mighty player
    self.slinky  = Slinky( pixelSize = 0.01 )
    self.addChild( 
      self.slinky, getsCollisions = True, collisionGroups = [0] 
    ) 
    self.slinky.move( 0, 0, 5 )
    # Give it a weight of 1 so it can be autoPushed
    self.slinky.weight = 1

    # Vertical distance between platforms
    self.smallIncrement = 1
    # How often new platforms will be added
    self.increment      = 5
    self.slinky.y  = -self.smallIncrement * 1.5
    self.lowest    = self.increment
    # The list of all platforms, they will be deleted when no used anymore
    self.platforms = []

  def updatePlatforms( self ):
    '''Create and delete platforms as needed'''
    # Do we need to create new platforms?
    if self.slinky.y < self.lowest - self.increment / 2.0:
      self.lowest -= self.increment
      # Create new platforms every self.smallIncrement meters
      for y in xrange( self.lowest, self.lowest - self.increment, -self.smallIncrement ):
        p = pig.Actor()
        # Randomly create 2 kinds of platform
        if random.randrange( 0, 5 ) < 4:
          p.addView( "main", pig.Image( "images/simple_platform.png"), pixelSize = 0.01 )
        else:
          p.addView( "main", pig.Image( "images/fragile_platform.png"), pixelSize = 0.01 )
          p.id = "breakable"
        p.move( random.randrange( -4, 3 ), y, 5 )
        self.addChild( p, collisionGroups = [0] )
        if len( self.platforms ) == 0:
          p.x = 0
        self.platforms.append( p )
      # Delete platforms that won't be visible anymore
      while True:
        if self.platforms[0].y > self.lowest + self.increment:
          p = self.platforms.pop( 0 )
          self.removeChild( p )
        else:
          break

  def update( self, time, elapsed ):
    self.updatePlatforms()
    # Compute the y position for our camera
    y = min( self.lowest + self.increment / 2.0, self.slinky.y )
    self.camera.y = y
    # If slinky is below the lowest platform, we have died
    if self.slinky.y > self.lowest + self.increment + self.increment / 2.0:
      return 1

  def draw( self, screen ):
    screen.fill( (255, 255, 255 ) )
    self.camera.draw( screen )

