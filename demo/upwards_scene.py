# -*- coding:utf-8 -*-

import random
import pygame
import pig
from wolverine import *

class UpwardsScene( pig.Scene ):
  def __init__( self, width, height ):
    pig.Scene.__init__( self, width, height )
    self.camera  = pig.FlatCamera( self, width, height, isometric = True )
    self.camera.move( width / 2, height / 2 )
    self.actor  = Wolverine()
    self.addChild( 
      self.actor, getsCollisions = True, collisionGroups = [0]
    ) 
    self.actor.move( 0, 0, 150 )
    self.actor.vx = 50

    self.rock = pig.Actor()
    self.rock.addView(
      "still", pig.Image( "images/rock.png" )
    )
    self.rock.move( 4, 0, 150 )
    self.addChild( 
      self.rock, getsCollisions = False, collisionGroups = set( [0] ) 
    )

    for i in xrange( 5 ):
      tree = pig.Actor()
      tree.addView(
        "still", pig.Image( "images/tree.png" )
      )
      tree.move( random.randrange( 0, width ), 0, random.randrange( 50, 200 ) )
      self.addChild( tree )

  def draw( self, screen ):
    screen.fill( (255, 255, 255 ) )
    self.camera.draw( screen )

