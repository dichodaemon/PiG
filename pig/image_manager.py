# -*- coding:utf-8 -*-

import pygame
from utility import Data

class ImageManager( object ):
  def __init__( self ):
    self.images = {}

  def loadSingle( self, filename, inverse = False ):
    key = filename + ": inverse=%i" % inverse
    if not key in self.images:
      data  = Data()
      image = pygame.image.load( filename ).convert_alpha()
      if inverse:
        image = pygame.transform.flip( image, True, False )
      data.image = image
      data.rect  = image.get_rect()
      data.tightImage = image.subsurface( image.get_bounding_rect() )
      data.tightRect  = data.tightImage.get_rect()
      self.images[key] = data
    return key

  def block( self, width, height, color ):
    key = "block: width=%i, height=%i" % ( width, height )
    key += " (r:%i, g:%i, b:%i, a:%i)" % color
    print key
    if not key in self.images:
      data  = Data()
      image = pygame.Surface( ( width, height ) ).convert_alpha()
      image.fill( color )
      data.image = image
      data.rect  = image.get_rect()
      data.tightImage = image.subsurface( image.get_bounding_rect() )
      data.tightRect  = data.tightImage.get_rect()
      self.images[key] = data
    return key

  def loadMulti( self, filename, count, inverse = False ):
    keys = [
      filename + ": count=%i, inverse=%i, frame=%i" % ( count, inverse, i)
      for i in xrange( count )
    ]
    if not keys[0] in self.images:
      full = pygame.image.load( filename ).convert_alpha()
      width     = full.get_width() / count
      height    = full.get_height()
      indices = range( count )
      for i in indices:
        data  = Data()
        image = full.subsurface( ( i  * width, 0, width, height ) )
        if inverse:
          image = pygame.transform.flip( image, True, False )
        data.image = image
        data.rect  = image.get_rect()
        data.tightImage = image.subsurface( image.get_bounding_rect() )
        data.tightRect  = data.tightImage.get_rect()
        self.images[keys[i]] = data
    return keys

  def scaled( self, key, width, height ):
    scaledKey = key + ", width=%i, height=%i" % ( width, height )
    try:
      return self.images[scaledKey]
    except KeyError:
      data = Data()
      image = pygame.transform.smoothscale( self.images[key].tightImage, (width, height ) )
      data.image = image
      data.rect  = image.get_rect()
      data.tightImage = image.subsurface( image.get_bounding_rect() )
      data.tightRect  = data.tightImage.get_rect()
      self.images[scaledKey] = data
      return data

manager = ImageManager()

def loadSingle( filename, inverse = False ):
  return manager.loadSingle( filename, inverse )

def block( width, height, color = (0, 0, 0, 0) ):
  return manager.block( width, height, color )

def loadMulti( filename, count, inverse = False ):
  return manager.loadMulti( filename, count, inverse )

def scaled( key, width, height ):
  return manager.scaled( key, width, height )

def image( key ):
  return manager.images[key]
