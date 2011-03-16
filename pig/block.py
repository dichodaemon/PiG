# -*- coding: utf-8 -*-

import pygame
import image_manager

class Block( object ):
  def __init__( self, width, height, color = ( 0, 0, 0, 0 ) ):
    self.frame = image_manager.block( width, height, color )

  def start( self, time ):
    pass

  def finished( self ):
    return True

  def key( self ):
    return self.frame
