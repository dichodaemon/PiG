# -*- coding: utf-8 -*-

from movable import *
import pygame
from math import floor

class Camera( Movable ):
  def __init__( self, scene, width, height, focalLength, zOffset = 0, isometric = False ):
    Movable.__init__( self )
    self.drawList    = scene.drawList
    self.scene       = scene
    self.focalLength = focalLength
    self.zOffset     = zOffset
    self.isometric   = isometric
    self.width       = width
    self.height      = height
    self.pixelSize   = 0.035 / height
    self.rect = pygame.Rect( 0, 0, self.width, self.height )
    self.move( 0, 0 )

  def pointTo( self, other, xoffset = 0, yoffset = 0 ):
    self.x, self.y = other.getPosition()
    self.x += xoffset
    self.y += yoffset

  def move( self, x, y ):
    self.x = x
    self.y = y
    self.rect.center = (x, y)

  def inFrustum( self, o ):
    if o.moved() or self.moved() or not hasattr( o, "cameraImage" ):
      z = o.z + self.zOffset
      if self.focalLength == 0:
        f  =  self.zOffset
      else:
        f  = self.focalLength / (z * self.pixelSize )
      width  = int( o.rect.width  * o.pixelSize * f )
      height = int( o.rect.height * o.pixelSize * f )
      s      = pygame.transform.smoothscale( o.surface, (width, height) )
      o.cameraImage = s
      o.cameraRect  = s.get_rect()
      x, y = o.getPosition()
      y = self.scene.height - y
      if self.isometric:
        y += self.scene.height - o.z
      x1   = ( x - self.x ) * f + self.width  / 2.0
      y1   = ( y - self.scene.height - self.y ) * f + self.height / 2.0
      o.screenPos = (x1, y1 - height )
    return self.rect.colliderect( o.cameraRect )

  def drawObject( self, screen, o ):
    screen.blit( o.cameraImage, o.screenPos )

  def draw( self, screen ):
    self.drawList.sort( key = lambda o: o.z, reverse = True )
    for o in self.drawList:
      if self.inFrustum( o ):
        self.drawObject( screen, o )

