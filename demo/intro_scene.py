# -*- coding:utf-8 -*-

import pygame
import pig

class IntroScene( pig.Scene ):
  def __init__( self, width, height ):
    pig.Scene.__init__( self, width, height )
    self.image  = pygame.image.load( "images/pig_logo.png" ) 

    self.duration = 0.1
    self.b1     = (0, 0, 0)
    self.b2     = (255, 255, 255)
    self.sound  = pygame.mixer.Sound( "sounds/vinyloink.wav" )

  def start( self, time ):
    self.sound.play()

  def update( self, time, elapsed ):
    self.background = pig.lerp( self.b1, self.b2, self.duration, time - self.startTime )
    if time - self.startTime >= self.duration:
      return 1
    return 0

  def draw( self, screen ):
    screen.fill( self.background )
    screen.blit( self.image, (0, 0) )

  def onKeyDown( self, key ):
    if key == "o":
      self.sound.play()

