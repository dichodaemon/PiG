# -*- coding:utf-8 -*-

import pygame
from utility import *

class Scene( object ):
  def __init__( self, width, height ):
    self.started    = False
    self.startTime  = 0
    self.objects    = {}
    self.drawList   = []
    self.collidable     = set([])
    self.getsCollisions = set([])
 
  def addChild( self, child, getsCollisions=False, collisionGroups = [], collisionsIn = [], collisionsOut = [] ):
    collisionsIn  = set( collisionsIn )
    collisionsOut = set( collisionsOut )
    data = Data()
    data.collidable = False
    self.drawList.append( child )
    if getsCollisions:
      collisionsIn.update( collisionGroups )
    collisionsOut.update( collisionGroups )
    if len( collisionsIn ) > 0 or len( collisionsOut ) > 0:
      data.object = child
      self.collidable.add( data )
      data.collidable = True
      data.collisionsIn = 0
      for v in collisionsIn:
        data.collisionsIn |= 1 << v
      data.collisionsOut = 0
      for v in collisionsOut:
        data.collisionsOut |=  1 << v
      if  len( collisionsIn ) > 0:
        self.getsCollisions.add( data )
    if self.started:
      child.start( self.time )
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
    for d1 in self.getsCollisions:
      c = d1.object
      for d2 in self.collidable:
        o = d2.object
        if (    d1.collisionsIn & d2.collisionsOut > 0
            and c != o and c.collides( o ) 
            and abs( c.z - o.z ) <= ( c.thickness + o.thickness ) / 2.0
        ):
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
    self.time = time

  def _update( self, time, elapsed ):
    if elapsed != 0:
      print 1.0 / elapsed
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
      for c1 in c.children:
        if hasattr( c1, "update" ):
          c1.update( time, elapsed )
    self.updateRectangles()
    self.checkCollisions()
    self.updateRectangles()
    for c in self.children:
      if c.remove:
        self.removeChild( c )
    self.time = time
    return result
 
  def updateRectangles( self ):
    for c in self.children:
      if c.moved():
        c.updateRectangles()

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
  
