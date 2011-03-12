# -*- coding: utf-8 -*-

class Movable( object ):
  def __init__( self ):
    self.__x   = 0
    self.__y   = 0
    self.__z   = 0
    self.oldX  = 0.1
    self.oldY  = 0.1
    self.oldZ  = 0.1

  def moveReset( self ):
    self.oldX = self.__x
    self.oldY = self.__y
    self.oldZ = self.__z

  def setX( self, value ):
    self.oldX = self.__x
    self.__x = value

  def getX( self ):
    return self.__x

  x = property( getX, setX )

  def setY( self, value ):
    self.oldY = self.__y
    self.__y = value

  def getY( self ):
    return self.__y

  y = property( getY, setY )

  def setZ( self, value ):
    self.oldZ = self.__z
    self.__z = value

  def getZ( self ):
    return self.__z

  z = property( getZ, setZ )

  def getPosition( self ):
    return self.x, self.y

  def moveDelta( self, dx, dy, dz = 0 ):
    self.x += dx
    self.y += dy
    self.z += dz

  def move( self, x, y, *args ):
    self.x = x
    self.y = y
    if len( args ) == 1:
      self.z = args[0]

  def moved( self ):
    return self.__x != self.oldX or self.__y != self.oldY

  def movedZ( self ):
    return self.__z != self.oldZ
