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
        data.getsCollisions = True
        self.getsCollisions.add( data )
      else:
        data.getsCollisions = False
    if self.started:
      if not child.started:
        child.start( self.time )
    self.objects[child] = data

  def removeChild( self, child ):
    try:
      data = self.objects[child]
      del self.objects[child]
      self.drawList.remove( child )
      if data.collidable:
        self.collidable.remove( data )
        if data.getsCollisions:
          self.getsCollisions.remove( data )
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
            and (
                 c.z > o.z and c.z < o.z + o.thickness
              or o.z > c.z and o.z < c.z + c.thickness
            )
        ):
          if hasattr( c, "onCollide" ):
            c.onCollide( o )

  def _start( self, time ):
    self.started   = True
    self.startTime = time
    if hasattr( self, "start" ):
      self.start( time )
    for c in self.children:
      if not c.started:
        if hasattr( c, "start" ):
          c.start( time )
    self.time = time

  def _update( self, time, elapsed ):
    self.time = time
    result = 0
    if not self.started:
      return result
    if hasattr( self, "update" ):
      result = self.update( time, elapsed )
    for c in self.children:
      r = c._update( time, elapsed )
      if r != None and r != 0:
        result = r
    self.updateRectangles()
    self.checkCollisions()
    self.updateRectangles()
    for c in self.children:
      if c.remove:
        self.removeChild( c )
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
  
