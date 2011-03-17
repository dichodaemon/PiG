# -*- coding: utf-8 -*-

import pygame
import image_manager

class Animation( object ):
  def __init__( self, filename, count, fps, inverse = False, loop = True ):
    self.frames = image_manager.loadMulti( filename, count, inverse )
    self.count     = count
    self.fps       = fps
    self.startTime = 0
    self.frame     = 0
    self.loop      = loop
    self.finished  = True
    self.started   = False

  def start( self, time ):
    self.started   = True
    self.startTime = time
    self.finished  = False

  def key( self ):
    return self.frames[self.frame]

  def update( self, time, delta ):
    self.frame = int( ( time - self.startTime ) * self.fps )
    if self.frame >= self.count and not self.loop:
      self.frame    = self.count - 1
      self.finished = True
    else:
      self.frame = self.frame % self.count
    return 0
