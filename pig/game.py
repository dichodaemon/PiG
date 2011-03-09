# -*- coding:utf-8 -*-

import pygame
import time

class Game( object ):
  def __init__( self, width, height, name, fps ):
    self.width        = width
    self.height       = height
    self.name         = name
    self.fps          = fps
    self.time         = 0
    self.lastTime     = 0
    self.paused       = False

    pygame.init()
    pygame.mixer.init()
    self.screen = pygame.display.set_mode( (width, height), 0, 32 )

    self.currentScene = 0
    self.scenes       = []
    self.transitions  = []

  def start( self ):
    self.scenes[0].start( self.time )

  def addScene( self, scene ):
    number = len( self.scenes )
    self.scenes.append( scene )
    self.transitions.append( {} )
    return number

  def setTransition( self, code, scene1, scene2 ):
    '''Specifies a transition from scene1 to scene 2 on the given code'''
    self.transitions[scene1][code] = scene2  

  def getScene( self ):
    scene = self.scenes[self.currentScene]
    scene._start( self.time )
    return scene

  def frameStart( self ):
    elapsed = 0
    current = time.time()
    if not self.paused and self.lastTime != 0:
      elapsed = current - self.lastTime
    self.lastTime = current
    self.time    += elapsed
    return elapsed

  def frameEnd( self ):
    current   = time.time()
    elapsed   = current - self.lastTime
    sleepTime = 1.0 / self.fps - elapsed 
    if sleepTime > 0:
      time.sleep( sleepTime )

  def processEvents( self ):
    currentScene = self.getScene()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return False
      elif event.type == pygame.KEYDOWN:
         currentScene._onKeyDown( pygame.key.name( event.key ) )
      elif event.type == pygame.KEYUP:
         currentScene._onKeyUp( pygame.key.name( event.key ) )
      elif event.type == pygame.MOUSEMOTION:
        x, y = event.pos
        currentScene._onMouseMove( x, y, event.buttons )
      elif event.type == pygame.MOUSEBUTTONUP:
        x, y = event.pos
        currentScene._onMouseUp( x, y, event.button )
      elif event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        currentScene._onMouseDown( x, y, event.button )
    return True

  def update( self, elapsed ):
    code = self.getScene()._update( self.time, elapsed )
    while code in self.transitions[self.currentScene]:
      #TODO: Take a closer look to this
      self.currentScene = self.transitions[self.currentScene][code]
      self.getScene()._start( self.time )
      code = self.getScene()._update( self.time, elapsed )
    if code != 0 and code != None:
      return False
    return True

  def draw( self ):
    self.getScene()._draw( self.screen )
    pygame.display.flip()

  def step( self ):
    elapsed = self.frameStart()
    ok = self.processEvents()
    ok = ok and self.update( elapsed )
    self.draw()
    self.frameEnd()
    return ok

  def run( self ):
    self.start()
    while True:
      if not self.step():
        break
    pygame.quit()
