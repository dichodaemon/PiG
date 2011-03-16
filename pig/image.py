# -*- coding: utf-8 -*-

import pygame
import image_manager

class Image( object ):
  def __init__( self, filename, inverse = False ):
    self.frame = image_manager.loadSingle( filename, inverse )

  def start( self, time ):
    pass

  def finished( self ):
    return True

  def key( self ):
    return self.frame
