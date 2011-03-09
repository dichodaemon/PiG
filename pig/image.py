# -*- coding: utf-8 -*-

import pygame

class Image( object ):
  def __init__( self, filename, inverse = False ):
    self.image = pygame.image.load( filename ).convert_alpha()
    if inverse:
      self.image = pygame.transform.flip( self.image, True, False )
    self.rect    = self.image.get_bounding_rect()
    self.surface = self.image.subsurface( self.rect )
    self.rect    = self.image.get_rect()
