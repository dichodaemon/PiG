# -*- coding:utf-8 -*-

import random
import pygame
import pig
from wolverine import *

class PlatformScene( pig.Scene ):
  def __init__( self, width, height ):
    pig.Scene.__init__( self, width, height )
    self.camera = pig.Camera( self, width, height, focalLength = 0.035, zOffset = 0 )
    self.actor  = Wolverine( pixelSize = 1.7 / 53 )
    self.addChild( 
      self.actor, getsCollisions = True, collisionGroups = [0] 
    ) 
    self.actor.move( 0, 0, 10 )
    self.actor.weight = 1

    self.rock = pig.Actor()
    self.rock.addView(
      "still", pig.Image( "images/rock.png" ), pixelSize = 1.70 / 53
    )
    self.rock.move( 4, 0, 10 )
    self.rock.weight = 1
    self.addChild( 
      self.rock, getsCollisions = False, collisionGroups = [0]
    )
    mountain = pig.Actor()
    mountain.addView(
      "still", pig.Image( "images/mountain.png" ), pixelSize = 0.5
    )
    mountain.move( -100, 0, 150 )
    self.addChild( mountain )

    current = -100
    while True:
      current  += random.randrange( 3, 10 )
      tree = pig.Actor()
      tree.addView(
        "still", pig.Image( "images/tree.png" ), pixelSize = 0.02
      )
      tree.move( current, -0.1 + random.random() * 0.2, 15 )
      self.addChild( tree )
      if current > 200: 
        break
    door = pig.Actor()
    door.addView( 
      "still", pig.Image( "images/door.png" ), pixelSize = 1.70 / 53
    )
    door.id = "door1"
    self.addChild(
      door, getsCollisions = False, collisionGroups = [0]
    )
    door.move( 10, 0, 10 )
    door = pig.Actor()
    door.addView( 
      "still", pig.Image( "images/door.png" ), pixelSize = 1.70 / 53
    )
    door.id = "door2"
    self.addChild(
      door, getsCollisions = False, collisionGroups = [0]
    )
    door.move( -4, 0, 10 )

  def draw( self, screen ):
    screen.fill( (255, 255, 255 ) )
    self.camera.pointTo( self.actor, 0.5, -1 )
    self.camera.draw( screen )

