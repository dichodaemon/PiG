# -*- coding:utf-8 -*-

import pygame

import image_manager
from animation  import *
from utility import *

from movable import *

class Actor( Movable ):
  def __init__( self ):
    Movable.__init__( self )
    self.id     = ""
    self.remove = False
    self.views  = {}
    self.move( 0, 0 )
    self.thickness = 0.1
    self.viewChanged = False
    self.currentName = None
    self.current = None
    self.started = False

  def start( self, time ):
    self.started = True
    self.startTime = time
    self.time = time
    self.updateRectangles()
    if not self.current.started:
      self.current.start( time )

  def getChildren( self ):
    return self.views.values()
  children = property( getChildren )

  def getPixelSize( self ):
    return self.current.pixelSize
  pixelSize = property( getPixelSize )

  def collides( self, other ):
    return self.rect.colliderect( other.rect )

  def addView( self, name, view, pixelSize = 1 ):
    view.pixelSize = pixelSize
    self.views[name] = view
    if len( self.views ) == 1:
      self.setView( name )

  def setView( self, name ):
    if self.current != self.views[name]:
      self.viewChanged = True
      self.currentName = name
      self.current     = self.views[name]
      if self.started and not self.current.started:
        self.current.start( self.time )

  def updateRectangles( self ):
    image = image_manager.image( self.current.key() )
    r = image.tightRect
    p = self.current.pixelSize * 100
    self.rect =  pygame.Rect( self.x * 100, self.y * 100, r.width * p, r.height * p )

  def key( self ):
    return self.current.key()

  def _update( self, time, elapsed ):
    self.time = time
    if hasattr( self, "update" ):
      self.update( time, elapsed )
    if hasattr( self.current, "update" ):
      self.current.update( time, elapsed )
    return 0
