# -*- coding: utf-8 -*-

import pygame

class Animation( object ):
  def __init__( self, filename, count, fps, inverse = False ):
    self.image = pygame.image.load( filename ).convert_alpha()
    if inverse:
      self.image = pygame.transform.flip( self.image, True, False )
    self.width     = self.image.get_width() / count
    self.height    = self.image.get_height()
    self.count     = count
    self.fps       = fps
    self.inverse   = inverse
    self.startTime = 0
    self.rects     = []
    self.images    = []
    self.frame     = 0
    indices = range( count )
    if inverse:
      indices.reverse()
    for i in indices:
      s = self.image.subsurface( ( i  * self.width, 0, self.width, self.height ) )
      r = s.get_bounding_rect()
      s = s.subsurface( r )
      self.images.append( s )
      self.rects.append( s.get_rect() )

  def start( self, time ):
    self.startTime = time

  def getRect( self ):
    return self.rects[self.frame]
  rect = property( getRect )

  def getSurface( self ):
    return self.images[self.frame]
  surface = property( getSurface )

  def update( self, time, delta ):
    self.frame = int( ( time - self.startTime ) * self.fps ) % self.count
    if self.inverse:
      self.frame = self.count - self.frame - 1
    return 0
