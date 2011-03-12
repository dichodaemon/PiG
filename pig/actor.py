# -*- coding:utf-8 -*-

import pygame
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

  def getRect( self ):
    r = self.current.rect
    p = self.current.pixelSize * 100
    return pygame.Rect( self.x * 100, self.y * 100 - r.height * p, r.width * p, r.height * p )
  rect = property( getRect )

  def getSurface( self ):
    return self.current.surface
  surface = property( getSurface )

  def _update( self, time, elapsed ):
    if hasattr( self.current, "update" ):
      self.current.update( time, elapsed )
    return 0

  def _onCollide( self, other ):
    pass

  def __getattribute__( self, name ):
    try:
      f1 = object.__getattribute__( self, "_" + name )
      f2 = None
      try:
        f2 = object.__getattribute__( self, name )
      except AttributeError:
        pass
      def result( *args, **kargs ):
        r = f1( *args, **kargs )
        if f2:
          r = f2( *args, **kargs )
        for c in self.children:
          if hasattr( c, name ):
            getattr( c, name )( *args, **kargs )
        return r
      return result
    except AttributeError, e:
      return object.__getattribute__( self, name )

