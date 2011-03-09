# -*- coding:utf-8 -*-

import pygame
from utility import *

class Scene( object ):
  def __init__( self, width, height ):
    self.started    = False
    self.startTime  = 0
    self.width      = width
    self.height     = height
    self.objects    = {}
    self.drawList   = []
    self.collidable     = set([])
    self.getsCollisions = set([])
 
  def addChild( self, child, getsCollisions=False, collisionGroups = None ):
    data = Data()
    data.collidable = False
    self.drawList.append( child )
    if collisionGroups and len( collisionGroups ) > 0:
      self.collidable.add( child )
      data.collidable = True
      data.getsCollisions  = getsCollisions
      data.collisionGroups = collisionGroups
      if getsCollisions:
        self.getsCollisions.add( child )
    self.objects[child] = data

  def removeChild( self, child ):
    try:
      data = self.objects[child]
      del self.objects[child]
      self.drawList.remove( child )
      if data.collidable:
        self.collidable.remove( child )
        if data.getsCollisions:
          self.getsCollisions.remove( child )
    except KeyError:
      pass

  def getChildren( self ):
    return self.objects.keys()
  children = property( getChildren )

  def checkCollisions( self ):
    for c in self.getsCollisions:
      for o in self.collidable:
        if c != o and c.collides( o ) and abs( c.z - o.z ) <= ( c.thickness + o.thickness ) / 2.0:
          if hasattr( c, "onCollide" ):
            c.onCollide( o )

  def _start( self, time ):
    if self.started:
      return
    self.started   = True
    self.startTime = time
    if hasattr( self, "start" ):
      self.start( time )
    for c in self.children:
      if hasattr( c, "start" ):
        c.start( time )

  def _update( self, time, elapsed ):
    result = 0
    if not self.started:
      return result
    if hasattr( self, "update" ):
      result = self.update( time, elapsed )
    for c in self.children:
      if hasattr( c, "update" ):
        r = c.update( time, elapsed )
        if r != None and r != 0:
          result = r
    self.checkCollisions()
    for c in self.children:
      if c.remove:
        self.removeChild( c )
    return result

  def __getattribute__( self, name ):
    try:
      return object.__getattribute__( self, name )
    except AttributeError, e:
      if name[0] == "_":
        f = None
        try:
          f = object.__getattribute__( self, name[1:] )
        except AttributeError:
          pass
        def result( *args, **kargs ):
          if f:
            f( *args, **kargs )
          for c in self.children:
            if hasattr( c, name[1:] ):
              getattr( c, name[1:] )( *args, **kargs )
        return result
      else:
        raise e

